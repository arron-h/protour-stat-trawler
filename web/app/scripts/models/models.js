App.Country = DS.Model.extend(
{
	name: DS.attr(),
	flagUrl: DS.attr()
});

App.Rider = DS.Model.extend(
{
	name: DS.attr(),
	weight: DS.attr(),
	height: DS.attr(),
	age: DS.attr(),
	country: DS.belongsTo('country')
});