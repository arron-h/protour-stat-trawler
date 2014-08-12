App.CountryCache =
{
	_cache: {},

	cache: function(countries)
	{
		countries.forEach(function(item)
		{
			_cache[item.get("id")] = item.get("name");
		});
	}
}