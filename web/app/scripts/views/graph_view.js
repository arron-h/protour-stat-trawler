App.GraphView = Ember.View.extend(
{
	/*
		--------------------------------------------------------------------------------------------------------
		COUNTRY REPRESENTATION GRAPH
		--------------------------------------------------------------------------------------------------------
	*/
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

	/*
		--------------------------------------------------------------------------------------------------------
		RIDER WEIGHT GRAPH
		--------------------------------------------------------------------------------------------------------
	*/
	graphRiderWeight: function()
	{
		var indices = {};
		var data    = [];

		var ranges =
		{
			"50-54": [ 50, 55],
			"55-59": [ 55, 60],
			"60-64": [ 60, 65],
			"65-69": [ 65, 70],
			"70-74": [ 70, 75],
			"75-79": [ 75, 80],
			"80-84": [ 80, 85],
			"85-89": [ 85, 90],
			"90-94": [ 90, 95]
		}

		var riders = this.get('controller.content');
		riders.forEach(function(item, index, enumerable)
		{
			var riderWeight = item.get("weight");

			if (riderWeight)
			{
				// Figure out which range the weight is in
				var riderWeightBand;
				for (var range in ranges)
				{
					if (riderWeight >= ranges[range][0] &&
						riderWeight < ranges[range][1])
					{
						riderWeightBand = range;
						break;
					}
				}

				if (!riderWeightBand)
					throw new Error("Failed to match weight band! Weight is: " + riderWeight);

				if (indices[riderWeightBand] === undefined)
				{
					var idx = data.push(
					{
						id:  riderWeightBand,
						count: 0
					}) - 1;
					indices[riderWeightBand] = idx;
				}

				var idx = indices[riderWeightBand];
				data[idx].count++;
			}
		});

		data.sort(function(a, b)
		{
			if (a.id < b.id)
				return -1;
			else if (a.id > b.id)
				return 1;
			return 0;
		});

		return data;
	},

	updateRiderWeightGraphData: function(svg, data)
	{
		svg.select(".axis").selectAll(".tick").data(data)
		svg.selectAll(".bar").data(data);
	},

	makeRiderWeightGraph: function(svg)
	{
        var data = this.graphRiderWeight();

        var margin = {top: 20, right: 20, bottom: 30, left: 40},
		    width = 500 - margin.left - margin.right,
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
			.attr("class", "x axis-label")
			.attr("transform", "translate(0," + height + ")")
			.append("text")
			.attr("y", 30)
			.attr("x", width/2)
			.text("Kilograms");

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
	},

	updateRiderWeightGraph: function()
	{
		var svg = d3.select("#riderWeightGraphSvg");

		if (svg.selectAll("rect").empty())
        {
        	this.makeRiderWeightGraph(svg);
        }
        else
        {
        	var data = this.graphRiderWeight();
        	this.updateRiderWeightGraphData(svg, data);
        }
	},

	/*
		--------------------------------------------------------------------------------------------------------
		RIDER HEIGHT GRAPH
		--------------------------------------------------------------------------------------------------------
	*/
	graphRiderHeight: function()
	{
		var indices = {};
		var data    = [];

		var ranges =
		{
			"1.50-1.54": [ 1.50, 1.55],
			"1.55-1.59": [ 1.55, 1.60],
			"1.60-1.64": [ 1.60, 1.65],
			"1.65-1.69": [ 1.65, 1.70],
			"1.70-1.74": [ 1.70, 1.75],
			"1.75-1.79": [ 1.75, 1.80],
			"1.80-1.84": [ 1.80, 1.85],
			"1.85-1.89": [ 1.85, 1.90],
			"1.90-1.94": [ 1.90, 1.95],
			"1.95-2.00": [ 1.95, 2.00],
		}

		var riders = this.get('controller.content');
		riders.forEach(function(item, index, enumerable)
		{
			var riderHeight = item.get("height");

			if (riderHeight)
			{
				// Figure out which range the height is in
				var riderHeightBand;
				for (var range in ranges)
				{
					if (riderHeight >= ranges[range][0] &&
						riderHeight < ranges[range][1])
					{
						riderHeightBand = range;
						break;
					}
				}

				if (!riderHeightBand)
					throw new Error("Failed to match weight band! Height is: " + riderHeight);

				if (indices[riderHeightBand] === undefined)
				{
					var idx = data.push(
					{
						id:  riderHeightBand,
						count: 0
					}) - 1;
					indices[riderHeightBand] = idx;
				}

				var idx = indices[riderHeightBand];
				data[idx].count++;
			}
		});

		data.sort(function(a, b)
		{
			if (a.id < b.id)
				return -1;
			else if (a.id > b.id)
				return 1;
			return 0;
		});

		return data;
	},

	updateRiderHeightGraphData: function(svg, data)
	{
		svg.select(".axis").selectAll(".tick").data(data)
		svg.selectAll(".bar").data(data);
	},

	makeRiderHeightGraph: function(svg)
	{
        var data = this.graphRiderHeight();

        var margin = {top: 20, right: 20, bottom: 30, left: 40},
		    width = 550 - margin.left - margin.right,
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
			.attr("class", "x axis-label")
			.attr("transform", "translate(0," + height + ")")
			.append("text")
			.attr("y", 30)
			.attr("x", width/2)
			.text("Meters");

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
	},

	updateRiderHeightGraph: function()
	{
		var svg = d3.select("#riderHeightGraphSvg");

		if (svg.selectAll("rect").empty())
        {
        	this.makeRiderHeightGraph(svg);
        }
        else
        {
        	var data = this.graphRiderHeight();
        	this.updateRiderHeightGraphData(svg, data);
        }
	},

	watchForGraphChanges: function()
	{
        setTimeout(this.updateCountryRepGraph.bind(this),
        	1000);

        setTimeout(this.updateRiderWeightGraph.bind(this),
        	1500);

        setTimeout(this.updateRiderHeightGraph.bind(this),
        	2000);
    }.observes("controller.length")
});