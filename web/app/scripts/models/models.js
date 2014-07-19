App.Country = DS.Model.extend(
{
	name: DS.attr()
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
	countryRep: DS.belongsTo('country'),
	averageAge: DS.attr(),
	averageWeight: DS.attr(),
	averageHeight: DS.attr()
});