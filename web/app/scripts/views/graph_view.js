App.GraphView = Ember.View.extend(
{
	graphCountryRepresentation: function()
	{
		var indices = {};
		var data    = [];

		var riders = this.get('controller.content');
		riders.forEach(function(item, index, enumerable)
		{
			var riderCountryId   = item.get("country").get("id");
			var riderCountryName = item.get("country").get("name");

			if (riderCountryId)
			{
				if (indices[riderCountryId] === undefined)
				{
					var idx = data.push(
					{
						id:  riderCountryId,
						name: riderCountryName,
						count: 0
					}) - 1;
					indices[riderCountryId] = idx;
				}

				var idx = indices[riderCountryId];
				data[idx].count++;
			}
		});

		return data;
	},

	updateCountryRepGraphData: function(svg, data)
	{
		svg.select(".axis").selectAll(".tick").data(data)
		svg.selectAll(".bar").data(data);
	},

	makeCountryRepGraph: function(svg)
	{
        var data = this.graphCountryRepresentation();

        var margin = {top: 20, right: 20, bottom: 30, left: 40},
		    width = 1200 - margin.left - margin.right,
		    height = 300 - margin.top - margin.bottom;
        
        var x = d3.scale.ordinal()
    		.rangeRoundBands([0, width], .1);

		var y = d3.scale.linear()
    		.range([height, 0]);

 		var xAxis = d3.svg.axis()
		    .scale(x)
		    .orient("bottom");

		var yAxis = d3.svg.axis()
		    .scale(y)
		    .orient("left")
		    .ticks(10, "%");

		svg.attr("width", width + margin.left + margin.right)
			.attr("height", height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		x.domain(data.map(function(d)
			{ 
				return d.id;
			}));
		y.domain([0, d3.max(data, function(d)
			{ 
				return d.count;
			})]);

		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis);

		svg.append("g")
			.attr("class", "y axis")
			.call(yAxis)
			.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", 6)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("Riders");

		svg.selectAll(".bar")
			.data(data)
			.enter().append("rect")
			.attr("class", "bar")
			.attr("x", function(d) { return x(d.id); })
			.attr("width", x.rangeBand())
			.attr("y", function(d) { return y(d.count); })
  			.attr("height", function(d) { return height - y(d.count); });


  		var flagWidth = x.rangeBand();

  		// Add flag image as tick
    	svg.select(".axis").selectAll(".tick")
            .data(data)
            .append("svg:image")
            .attr("xlink:href", function(d) { return App.FlagUrlBuilder(d.name, flagWidth); })
            .attr("x", -flagWidth/2)
            .attr("y", 20)
            .attr("width", flagWidth)
            .attr("height", Math.round(flagWidth*0.6));
	},

	updateCountryRepGraph: function()
	{
		var svg = d3.select("#countryRepGraphSvg");

		if (svg.selectAll("rect").empty())
        {
        	this.makeCountryRepGraph(svg);
        }
        else
        {
        	var data = this.graphCountryRepresentation();
        	this.updateCountryRepGraphData(svg, data);
        }
	},

	watchForGraphChanges: function()
	{
        setTimeout(this.updateCountryRepGraph.bind(this),
        	1000);
    }.observes("controller.length")
});