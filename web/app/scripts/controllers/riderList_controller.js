App.RiderListController = Ember.ArrayController.extend(
{
	/**
	@property sortProperties
	Properties dictating the arrangedContent's sort order.
	*/
	sortProperties: ["age"],

	/**
	@property sortAscending
	The arrangedContent's sort direction.
	*/
	sortAscending: true,

	/**
	@property contentSetSize
	The number of results to show
	*/
	contentSetSize: 50,

	/**
	@method limitedContent
	Returns a limited set of results from the sorted array.
	*/
	limitedContent: function()
	{
		return this.get("arrangedContent").slice(0, this.get("contentSetSize"));
	}.property("arrangedContent.[]", "sortProperties", "sortAscending", "contentSetSize"),

	contentSetSizeChanged: function()
	{
		Ember.run.scheduleOnce('afterRender', this, function()
		{
    		$('[data-spy="scroll"]').each(function()
			{
				var $spy = $(this).scrollspy('refresh')
			});
  		});
	}.observes("contentSetSize"),

	shouldShowMore: function()
	{
		if (this.get("contentSetSize") == this.get("content.length"))
			return false;

		return true;
	}.property("contentSetSize"),

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
		},

		showMore: function()
		{
			var currentSize = this.get("contentSetSize");
			this.set("contentSetSize", currentSize + 50);
		},

		showAll: function()
		{
			this.set("contentSetSize", this.get("content.length"));	
		}
	}
});