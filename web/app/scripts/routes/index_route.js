App.IndexRoute = Ember.Route.extend(
{
	renderTemplate: function(controller, model) 
	{
		this._super(controller, model);

		this.render('riderlist',
		{
			into: 'index',
			outlet: 'riderlist',
			controller: 'riderList'
		});

		this.render('graph',
		{
			into: 'index',
			outlet: 'graph',
			controller: 'graph'
		});
	},

	setupController: function(controller, model)
	{
		this._super(controller, model);

		// Cache countries so they're available to the graphs
		App.CountryCache.cache(this.store.find('country'));

		var metrics = this.store.find('metrics', 0);
		controller.set('content',
		{
			metrics: metrics,
			exportDate: App.EXPORT.Date
		});

		var riders = this.store.find('rider');

		this.controllerFor('riderList').set('content', riders);
		this.controllerFor('graph').set('content', riders);
	}
});
