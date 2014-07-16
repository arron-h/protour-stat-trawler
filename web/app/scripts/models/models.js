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

App.Metrics = DS.Model.extend(
{
	averageAge: DS.attr(),
	averageWeight: DS.attr(),
	averageHeight: DS.attr()
});