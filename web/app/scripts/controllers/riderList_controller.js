App.RiderListController = Ember.ArrayController.extend(
{
	/**
	@property sortProperties
	Properties dictating the arrangedContent's sort order.
	*/
	sortProperties: ['weight'],

	/**
	@property sortAscending
	The arrangedContent's sort direction.
	*/
	sortAscending: true
});