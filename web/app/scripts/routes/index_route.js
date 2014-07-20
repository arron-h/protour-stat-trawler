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
	},

	setupController: function(controller, model)
	{
		this._super(controller, model);

		var metrics = this.store.find('metrics', 0);
		controller.set('content', metrics);

		var riders = this.store.find('rider');
		this.controllerFor('riderList').set('content', riders);
	}
});
