App.IndexController = Ember.ObjectController.extend(
{
	avgAge: function()
	{
		var mdl = this.get("model");
		var t = 0;
		var c = 0;
		mdl.forEach(function(item,index,e)
		{
			t += item.get("age");
			c++;
		});
		
		return t/c;
	}.property('model'),

	something: "Hello"
});