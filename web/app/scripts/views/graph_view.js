App.GraphView = Ember.View.extend(
{
	graph_makeBarGraphBase: function(svg, width, height)
	{
		var axis = {};

		var margin = {top: 20, right: 20, bottom: 30, left: 40};

		axis.width = width - margin.left - margin.right;
		axis.height = height - margin.top - margin.bottom;

		axis.xRange = d3.scale.ordinal()
			.rangeRoundBands([0, axis.width], .1);

		axis.yRange = d3.scale.linear()
			.range([axis.height, 0]);

		axis.x = d3.svg.axis()
			.scale(axis.xRange)
			.orient("bottom");

		axis.y = d3.svg.axis()
			.scale(axis.yRange)
			.orient("left")
			.ticks(10, "%");

		svg.attr("width", axis.width + margin.left + margin.right)
			.attr("height", axis.height + margin.top + margin.bottom)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		return axis;	
	},

	graph_mapData: function(axis, data, xAxisData, yAxisData)
	{
		axis.xRange.domain(data.map(function(d)
			{ 
				return d[xAxisData];
			}));
		axis.yRange.domain([0, d3.max(data, function(d)
			{ 
				return d[yAxisData];
			})]);
	},

	graph_drawXAxis: function(svg, axis, label)
	{
		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + axis.height + ")")
			.call(axis.x);

		if (label)
		{
			svg.append("g")
				.attr("class", "x axis-label")
				.attr("transform", "translate(0," + axis.height + ")")
				.append("text")
				.attr("y", 30)
				.attr("x", axis.width/2)
				.text(label);
		}
	},

	graph_drawYAxis: function(svg, axis, label)
	{
		var elem = svg.append("g")
			.attr("class", "y axis")
			.call(axis.y);

		if (label)
		{
			elem.append("text")
				.attr("transform", "rotate(-90)")
				.attr("y", 6)
				.attr("dy", ".71em")
				.style("text-anchor", "end")
				.text(label);
		}
	},

	graph_drawBars: function(svg, data, axis, xAxisData, yAxisData)
	{
		svg.selectAll(".bar")
			.data(data)
			.enter().append("rect")
			.attr("class", "bar")
			.attr("x", function(d) { return axis.xRange(d[xAxisData]); })
			.attr("width", axis.xRange.rangeBand())
			.attr("y", function(d) { return axis.yRange(d[yAxisData]); })
			.attr("height", function(d) { return axis.height - axis.yRange(d[yAxisData]); });
	},

	generateRangedData: function(ranges, key)
	{
		var indices = {};
		var data    = [];

		var riders = this.get('controller.content');
		riders.forEach(function(item, index, enumerable)
		{
			var value = item.get(key);

			if (value)
			{
				// Figure out which range the weight is in
				var band;
				for (var range in ranges)
				{
					if (value >= ranges[range][0] &&
						value < ranges[range][1])
					{
						band = range;
						break;
					}
				}

				if (!band)
					throw new Error("Failed to match "+key+" band! Weight is: " + value);

				if (indices[band] === undefined)
				{
					var idx = data.push(
					{
						id:  band,
						count: 0
					}) - 1;
					indices[band] = idx;
				}

				var idx = indices[band];
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

	updateBarGraphData: function(svg, data)
	{
		svg.select(".axis").selectAll(".tick").data(data)
		svg.selectAll(".bar").data(data);
	},

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

	makeCountryRepGraph: function(svg)
	{
		var data = this.graphCountryRepresentation();

		var axis = this.graph_makeBarGraphBase(svg, 1200, 300);
		this.graph_mapData(axis, data, "id", "count");

		this.graph_drawXAxis(svg, axis, null);
		this.graph_drawYAxis(svg, axis, "Riders");

		this.graph_drawBars(svg, data, axis, "id", "count");

		var flagWidth = axis.xRange.rangeBand();

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
			this.updateBarGraphData(svg, data);
		}
	},

	/*
		--------------------------------------------------------------------------------------------------------
		RIDER WEIGHT GRAPH
		--------------------------------------------------------------------------------------------------------
	*/
	graphRiderWeight: function()
	{
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

		return this.generateRangedData(ranges, "weight");
	},

	makeRiderWeightGraph: function(svg)
	{
		var data = this.graphRiderWeight();

		var axis = this.graph_makeBarGraphBase(svg, 500, 300);
		this.graph_mapData(axis, data, "id", "count");

		this.graph_drawXAxis(svg, axis, "Kilograms");
		this.graph_drawYAxis(svg, axis, "Riders");

		this.graph_drawBars(svg, data, axis, "id", "count");
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
			this.updateBarGraphData(svg, data);
		}
	},

	/*
		--------------------------------------------------------------------------------------------------------
		RIDER HEIGHT GRAPH
		--------------------------------------------------------------------------------------------------------
	*/
	graphRiderHeight: function()
	{
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

		return this.generateRangedData(ranges, "height");
	},

	makeRiderHeightGraph: function(svg)
	{
		var data = this.graphRiderHeight();

		var axis = this.graph_makeBarGraphBase(svg, 500, 300);
		this.graph_mapData(axis, data, "id", "count");

		this.graph_drawXAxis(svg, axis, "Metres");
		this.graph_drawYAxis(svg, axis, "Riders");

		this.graph_drawBars(svg, data, axis, "id", "count");
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
			this.updateBarGraphData(svg, data);
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