from catalog.templatetags.catalog_tags import get_categories
from catalog import views
from warehouse_pr.tests import TestBasedModel


class TestGetCategoriesTag(TestBasedModel):
    def test_get_categories_tag_by_status(self):
        self.assertEqual(
            get_categories(), views.show_category)
