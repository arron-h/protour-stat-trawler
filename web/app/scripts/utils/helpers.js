Ember.Handlebars.helper('flagUrlImg', function(countryName, pxSize, options)
{
	var url = App.FlagUrlBuilder(countryName, pxSize);
 	return new Handlebars.SafeString(
  		"<img src='"+url+"' alt='"+countryName+"' title='"+countryName+"'/>");
});
