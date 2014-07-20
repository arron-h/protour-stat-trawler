App.FlagUrlHashes = {}

App.FlagUrlTransformers =
{
	"Republic of Ireland": "Ireland"
}

App.FlagUrlBuilder = function(country, size)
{
	if (!country)
	{
		return "";
	}

	// Handle edge cases
	if (App.FlagUrlTransformers[country])
	{
		country = App.FlagUrlTransformers[country];
	}

	// Url must have underscores
	country = country.replace(/\s/g, "_");

	if (App.FlagUrlHashes[country] && App.FlagUrlHashes[country][size])
	{
		return App.FlagUrlHashes[country][size];
	}
	
	// Calculates the flag url
	var filename = "Flag_of_"+country+".svg";
	var hash     = CryptoJS.MD5(filename).toString();
	var hashedComponents = hash[0]+"/"+hash[0]+hash[1]

	var url = "http://upload.wikimedia.org/wikipedia/commons/thumb/" +
		hashedComponents + "/" + filename + "/" +
		size + "px-" + filename + ".png";

	App.FlagUrlHashes[country] = {};
	App.FlagUrlHashes[country][size] = url;

	return url;
}