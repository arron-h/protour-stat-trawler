App.RiderListController = Ember.ArrayController.extend(
{
	/**
	@property sortProperties
	Properties dictating the arrangedContent's sort order.
	*/
	sortProperties: ["weight"],

	/**
	@property sortAscending
	The arrangedContent's sort direction.
	*/
	sortAscending: true,

	actions:
	{
		sort: function(column)
		{
			if (this.get("sortProperties")[0] == column)
			{
				// Just swap
				this.set("sortAscending", !this.get("sortAscending"));
			}
			else
			{
				this.set("sortProperties", [column]);	
				this.get("sortAscending", true);
			}
		}
	}
});