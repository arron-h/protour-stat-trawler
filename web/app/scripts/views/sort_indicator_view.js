App.SortIndicatorView = Ember.View.extend(
{
	templateName: "sortindicator",

	columnName: function()
	{
		var columnName = this.get("column");
		columnName = columnName.charAt(0).toUpperCase() + columnName.slice(1);
		return columnName;
	}.property('column'),

	sortDirection: function()
	{
		var controller   = this.get("controller");
		var asc          = controller.get("sortAscending");
		var sorter       = controller.get("sortProperties");
		var sortedColumn = sorter[0];

		if (this.get("column") != sortedColumn)
		{
			return "";
		}

		var classSelectors  = "glyphicon ";
		if (asc)
			classSelectors += "glyphicon-chevron-up";
		else
			classSelectors += "glyphicon-chevron-down";

		return classSelectors;
	}.property("controller.sortAscending", "controller.sortProperties")
});