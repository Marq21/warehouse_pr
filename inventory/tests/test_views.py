from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from inventory.models import InventoryItem, InventoryTask, NomenclatureRemain
from catalog.models import Category, Nomenclature
from inventory.forms import CreateInventoryTaskForm, InputBarcodeForm, UpdateStatusForm
from django.contrib import messages
from inventory.views import CreateInventoryTask

from warehouse_pr.tests import TestBasedModel


class QuantityListViewTest(TestBasedModel):

    def setUp(self) -> None:
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        return super().setUp()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('list_of_quantity'))
        self.assertEqual(resp.status_code, 200)

    def test_view_nom_list_template_used(self):
        resp = self.client.get(reverse('list_of_quantity'))
        self.assertTemplateUsed(
            resp, 'inventory/list_of_remaining_quantities.html')

    def test_home_view(self):
        resp = self.client.get(
            "/inventory/list_of_quantity/", {'quantity_list': NomenclatureRemain.objects.all()})
        self.assertEqual(resp.status_code, 200)


class InventoryTaskViewTest(TestBasedModel):

    def setUp(self) -> None:
        category = Category.objects.last()
        self.factory = RequestFactory()
        self.inv_task = InventoryTask.objects.create(
            name='test_inventory_for_view',
            category=category,
        )
        self.inv_item = InventoryItem.objects.create(
            nomenclature=Nomenclature.objects.last(),
            inventory_task=self.inv_task,
        )
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        for nom in Nomenclature.objects.all():
            nom.category = category
            nom.save()
        return super().setUp()

    def test_delete_view_get_context(self):
        resp = self.client.get(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}/delete/")
        resp.user = self.user
        self.assertIsInstance(resp.context_data, dict)
        self.assertEqual(
            resp.context_data['title'], "Удалить задание на пересчёт")

    def test_create_view_POST_success_form_valid(self):
        category = Category.objects.last()
        data = {
            'name': 'inventory_task_view_test',
            'category': category,
        }
        nomenclature_list = list(
            Nomenclature.objects.filter(category=category))
        form = CreateInventoryTaskForm(data)

        request = self.factory.post(
            '/inventory/create_inventory_task/', data=data)
        request.user = self.user
        request._messages = messages.storage.default_storage(request)

        add_view = CreateInventoryTask()
        add_view.setup(request)

        self.assertTrue(add_view.form_valid(form=form))

        inventory_item_list = list(InventoryItem.objects.filter(inventory_task=InventoryTask.objects.get(
            name='inventory_task_view_test')))

        self.assertEqual(len(inventory_item_list), len(nomenclature_list))
        self.assertTrue(InventoryTask.objects.get(
            name='inventory_task_view_test'))

    def test_inventory_task_confirm_view(self):
        resp = self.client.post(
            f"/inventory/accept_task/confirm/{self.inv_task.pk}")
        self.assertTrue(
            resp.context['title'], 'Подтвердите завершение пересчета')
        self.assertIsInstance(
            resp.context['compared_confirm_list'], zip)
        self.assertEqual(
            resp.context['task_id'], self.inv_task.pk
        )

    def test_call_view_deny_anonymous(self):
        self.client.logout()
        response = self.client.get(
            f"/inventory/accept_task/confirm/{self.inv_task.pk}", follow=True)
        self.assertRedirects(
            response, f'/accounts/login/?next=/inventory/accept_task/confirm/{self.inv_task.pk}')
        response = self.client.post(
            f"/inventory/accept_task/confirm/{self.inv_task.pk}", follow=True)
        self.assertRedirects(
            response, f'/accounts/login/?next=/inventory/accept_task/confirm/{self.inv_task.pk}')

    def test_inventory_task_done(self):
        resp = self.client.post(
            f"/inventory/accept_task/done/{self.inv_task.pk}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['title'],
                         f'Задание № {self.inv_task.pk} завершено')
        self.assertEqual(resp.context['inventory_task'], self.inv_task)
        self.assertIsInstance(resp.context['nomenclature_remain_list'],
                              list)

    def test_inventory_task_detai_formed_status(self):
        self.inv_task.status = InventoryTask.InventoryStatus.FORMED
        resp = self.client.get(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context['title'], f'Задание на пересчёт: {self.inv_task} №{self.inv_task.pk} ')
        self.assertIsInstance(resp.context['inventory_item_list'], list)
        self.assertIsInstance(resp.context['form'], UpdateStatusForm)
        self.assertEqual(resp.context['task'], self.inv_task)

        resp = self.client.post(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}")
        self.assertRedirects(resp, reverse(
            'inventory-task-detail', kwargs={'pk': self.inv_task.pk}))

    def test_inventory_task_detai_in_progress_status(self):

        self.inv_task.status = InventoryTask.InventoryStatus.IN_PROGRESS
        self.inv_task.save()
        resp = self.client.get(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context['title'], f'Задание на пересчёт: {self.inv_task} №{self.inv_task.pk} ')
        self.assertIsInstance(resp.context['inventory_item_list'], list)
        self.assertIsInstance(resp.context['form'], InputBarcodeForm)
        self.assertEqual(resp.context['task'], self.inv_task)

        data = {
            'barcode_input': self.inv_item.nomenclature.barcode,
        }

        item_id = self.inv_item.id
        request = self.client.post(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}", data=data, follow=True)

        self.assertEqual(request.redirect_chain[0][1], 301)
        self.assertRedirects(
            request, f'/inventory/inventory_item/{item_id}', status_code=301)

    def test_inventory_task_detail_done_status(self):
        self.inv_task.status = InventoryTask.InventoryStatus.DONE
        self.inv_task.save()
        resp = self.client.get(
            f"/inventory/inventory_task_detail/{self.inv_task.pk}", follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)
        self.assertRedirects(
            resp, f'/inventory/accept_task/done/{self.inv_task.pk}')

    def test_item_update_view_get_success_url(self):
        resp = self.client.post(
            f"/inventory/inventory_item/{self.inv_item.pk}", follow=True)
        self.assertRedirects(
            resp, reverse('inventory-task-detail',
                          args=[self.inv_item.inventory_task.pk])
        )
