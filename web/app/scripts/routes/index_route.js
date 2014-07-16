App.IndexRoute = Ember.Route.extend({
	model: function()
	{
		return Ember.RSVP.hash({
			metrics: this.store.find('metrics', 0),
			riders: this.store.find('rider')
		});
	}
});
