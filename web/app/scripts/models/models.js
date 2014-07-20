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
	team: DS.attr(),
	country: DS.belongsTo('country')
});

App.Metrics = DS.Model.extend(
{
	countryRep: DS.belongsTo('country'),
	countryRepCount: DS.attr(),
	averageAge: DS.attr(),
	averageWeight: DS.attr(),
	averageHeight: DS.attr()
});