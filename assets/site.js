const datasetPath = "A359012.csv";

const colors = {
  accent: "#53f2c7",
  accent2: "#6ea8ff",
  accent3: "#ffb86b",
  muted: "#99abd6",
  text: "#eaf1ff",
};

const tooltip = d3
  .select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

const formatInt = d3.format(",");
const formatRatio = d3.format(".2f");
const formatDepth = d3.format(".3f");

d3.csv(datasetPath, d3.autoType)
  .then((rows) => {
    const data = rows
      .map((row) => ({
        ...row,
        repeatedDigits: new Set(String(row.k).split("")).size < String(row.k).length,
        palindrome: String(row.k) === String(row.k).split("").reverse().join(""),
        trailingZero: String(row.permutations).endsWith("0"),
      }))
      .sort((a, b) => d3.ascending(a.k, b.k));

    renderHeroStats(data);
    renderMetrics(data);
    renderLengthChart(data);
    renderSplitHeatmap(data);
    renderGrowthChart(data);
    renderScatterPlot(data);
    renderTable(data);
  })
  .catch((error) => {
    console.error(error);
    d3.select("#dashboard")
      .append("p")
      .text("Unable to load A359012.csv. Serve the project through a local web server so D3 can fetch the dataset.");
  });

function renderHeroStats(data) {
  const stats = [
    { label: "Terms", value: formatInt(data.length) },
    { label: "Max k", value: formatInt(d3.max(data, (d) => d.k)) },
    { label: "Longest witness", value: formatInt(d3.max(data, (d) => d["|permutations|"])) + " digits" },
  ];

  const container = d3.select("#hero-stats").html("");
  container
    .selectAll(".hero-stat")
    .data(stats)
    .join("article")
    .attr("class", "hero-stat")
    .html(
      (d) => `<span class="metric-label">${d.label}</span><strong>${d.value}</strong>`
    );
}

function renderMetrics(data) {
  const prefixHits = data.filter((d) => d.position_of_k === 0).length;
  const suffixHits = data.filter(
    (d) => d.position_of_k + String(d.k).length === d["|permutations|"]
  ).length;
  const metrics = [
    {
      label: "Trailing-zero witnesses",
      value: `${formatInt(data.filter((d) => d.trailingZero).length)}/${formatInt(data.length)}`,
      detail: "Permutation values end in zero for the overwhelming majority of terms.",
    },
    {
      label: "Repeated-digit terms",
      value: formatInt(data.filter((d) => d.repeatedDigits).length),
      detail: "Digit repetition is far more common than all-distinct terms in the current search window.",
    },
    {
      label: "Palindrome terms",
      value: formatInt(data.filter((d) => d.palindrome).length),
      detail: data.filter((d) => d.palindrome).map((d) => d.k).join(", ") || "None",
    },
    {
      label: "Prefix / suffix hits",
      value: `${prefixHits} / ${suffixHits}`,
      detail: "Most terms land strictly inside the witness value instead of at either edge.",
    },
  ];

  d3.select("#metric-grid")
    .selectAll(".metric-card")
    .data(metrics)
    .join("article")
    .attr("class", "metric-card")
    .html(
      (d) =>
        `<span class="metric-label">${d.label}</span><strong class="metric-value">${d.value}</strong><p class="metric-detail">${d.detail}</p>`
    );
}

function renderLengthChart(data) {
  const counts = d3.rollups(
    data,
    (values) => values.length,
    (d) => d["|k|"]
  )
    .map(([length, count]) => ({ length, count }))
    .sort((a, b) => d3.ascending(a.length, b.length));

  const container = d3.select("#length-chart");
  const width = container.node().clientWidth || 720;
  const height = 340;
  const margin = { top: 16, right: 18, bottom: 42, left: 52 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3
    .scaleBand()
    .domain(counts.map((d) => String(d.length)))
    .range([margin.left, width - margin.right])
    .padding(0.28);
  const y = d3
    .scaleLinear()
    .domain([0, d3.max(counts, (d) => d.count)])
    .nice()
    .range([height - margin.bottom, margin.top]);

  svg
    .append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0,0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .select(".domain")
    .remove();

  svg
    .selectAll(".bar")
    .data(counts)
    .join("rect")
    .attr("x", (d) => x(String(d.length)))
    .attr("y", (d) => y(d.count))
    .attr("width", x.bandwidth())
    .attr("height", (d) => y(0) - y(d.count))
    .attr("rx", 16)
    .attr("fill", "url(#lengthGradient)")
    .on("mousemove", (event, d) => showTooltip(event, `${d.length}-digit terms<br><strong>${formatInt(d.count)}</strong>`))
    .on("mouseleave", hideTooltip);

  const defs = svg.append("defs");
  const gradient = defs
    .append("linearGradient")
    .attr("id", "lengthGradient")
    .attr("x1", "0%")
    .attr("x2", "0%")
    .attr("y1", "0%")
    .attr("y2", "100%");
  gradient.append("stop").attr("offset", "0%").attr("stop-color", colors.accent);
  gradient.append("stop").attr("offset", "100%").attr("stop-color", colors.accent2);

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x));

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5));
}

function renderSplitHeatmap(data) {
  const xDomain = Array.from(new Set(data.map((d) => d["|x|"]))).sort(d3.ascending);
  const yDomain = Array.from(new Set(data.map((d) => d["|y|"]))).sort(d3.ascending);
  const counts = d3.rollups(
    data,
    (values) => values.length,
    (d) => d["|x|"],
    (d) => d["|y|"]
  );

  const cells = [];
  counts.forEach(([xLength, entries]) => {
    entries.forEach(([yLength, count]) => {
      cells.push({ xLength, yLength, count });
    });
  });

  const container = d3.select("#split-heatmap");
  const width = container.node().clientWidth || 540;
  const height = 340;
  const margin = { top: 20, right: 18, bottom: 50, left: 58 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleBand().domain(xDomain).range([margin.left, width - margin.right]).padding(0.14);
  const y = d3.scaleBand().domain(yDomain).range([height - margin.bottom, margin.top]).padding(0.14);
  const color = d3.scaleSequential([0, d3.max(cells, (d) => d.count)], d3.interpolateRgbBasis(["#0c1630", "#2458c7", "#53f2c7"]));

  svg
    .selectAll("rect")
    .data(cells)
    .join("rect")
    .attr("x", (d) => x(d.xLength))
    .attr("y", (d) => y(d.yLength))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("rx", 12)
    .attr("fill", (d) => color(d.count))
    .on("mousemove", (event, d) => showTooltip(event, `|x|=${d.xLength}, |y|=${d.yLength}<br><strong>${d.count} terms</strong>`))
    .on("mouseleave", hideTooltip);

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x));

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));

  svg
    .append("text")
    .attr("class", "chart-label")
    .attr("x", width / 2)
    .attr("y", height - 10)
    .attr("text-anchor", "middle")
    .text("|x|");

  svg
    .append("text")
    .attr("class", "chart-label")
    .attr("transform", `translate(18 ${height / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .text("|y|");
}

function renderGrowthChart(data) {
  const growth = data.map((d, index) => ({ k: d.k, count: index + 1 }));
  const container = d3.select("#growth-chart");
  const width = container.node().clientWidth || 540;
  const height = 340;
  const margin = { top: 18, right: 18, bottom: 42, left: 56 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleLinear().domain(d3.extent(growth, (d) => d.k)).range([margin.left, width - margin.right]);
  const y = d3.scaleLinear().domain([1, d3.max(growth, (d) => d.count)]).range([height - margin.bottom, margin.top]);

  const line = d3
    .line()
    .x((d) => x(d.k))
    .y((d) => y(d.count))
    .curve(d3.curveMonotoneX);

  svg
    .append("path")
    .datum(growth)
    .attr("fill", "none")
    .attr("stroke", colors.accent3)
    .attr("stroke-width", 3)
    .attr("d", line);

  svg
    .selectAll("circle")
    .data(growth.filter((_, index) => index % 45 === 0 || index === growth.length - 1))
    .join("circle")
    .attr("cx", (d) => x(d.k))
    .attr("cy", (d) => y(d.count))
    .attr("r", 4)
    .attr("fill", colors.accent3)
    .on("mousemove", (event, d) => showTooltip(event, `k <= ${formatInt(d.k)}<br><strong>${formatInt(d.count)} cumulative terms</strong>`))
    .on("mouseleave", hideTooltip);

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(formatInt));

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5));
}

function renderScatterPlot(data) {
  const container = d3.select("#scatter-plot");
  const width = container.node().clientWidth || 920;
  const height = 520;
  const margin = { top: 18, right: 18, bottom: 50, left: 58 };
  const color = d3.scaleOrdinal().domain([3, 4, 5, 6]).range(["#53f2c7", "#6ea8ff", "#ffb86b", "#ff7a90"]);

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleLinear().domain(d3.extent(data, (d) => d.expansion_ratio)).nice().range([margin.left, width - margin.right]);
  const y = d3.scaleLinear().domain([0, 1]).range([height - margin.bottom, margin.top]);

  svg
    .append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0,0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .select(".domain")
    .remove();

  svg
    .selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", (d) => x(d.expansion_ratio))
    .attr("cy", (d) => y(d.relative_depth))
    .attr("r", 4.8)
    .attr("fill", (d) => color(d["|k|"]))
    .attr("fill-opacity", 0.72)
    .attr("stroke", "rgba(255,255,255,0.18)")
    .on(
      "mousemove",
      (event, d) =>
        showTooltip(
          event,
          `k=${d.k}<br>x=${d.x}, y=${d.y}<br>|P|=${formatInt(d["|permutations|"])}<br>depth=${formatDepth(d.relative_depth)}<br>ratio=${formatRatio(d.expansion_ratio)}`
        )
    )
    .on("mouseleave", hideTooltip);

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(6));

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5));

  svg
    .append("text")
    .attr("class", "chart-label")
    .attr("x", width / 2)
    .attr("y", height - 10)
    .attr("text-anchor", "middle")
    .text("Expansion ratio  |P(x,y)| / |k|");

  svg
    .append("text")
    .attr("class", "chart-label")
    .attr("transform", `translate(18 ${height / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .text("Relative depth");

  const legend = svg.append("g").attr("class", "legend").attr("transform", `translate(${width - 180}, ${margin.top + 8})`);
  [3, 4, 5, 6].forEach((length, index) => {
    const row = legend.append("g").attr("transform", `translate(0, ${index * 24})`);
    row.append("circle").attr("r", 6).attr("cx", 0).attr("cy", 0).attr("fill", color(length));
    row.append("text").attr("x", 14).attr("y", 4).text(`${length}-digit k`);
  });
}

function renderTable(data) {
  const searchInput = document.getElementById("search-input");
  const lengthFilter = document.getElementById("length-filter");
  const limitFilter = document.getElementById("limit-filter");
  const tableBody = d3.select("#sequence-table");
  const summary = d3.select("#table-summary");

  const lengths = Array.from(new Set(data.map((d) => d["|k|"]))).sort(d3.ascending);
  lengths.forEach((length) => {
    const option = document.createElement("option");
    option.value = String(length);
    option.textContent = `${length} digits`;
    lengthFilter.appendChild(option);
  });

  function updateTable() {
    const query = searchInput.value.trim().toLowerCase();
    const selectedLength = lengthFilter.value;
    const limit = Number(limitFilter.value);

    const filtered = data.filter((row) => {
      const matchesLength = selectedLength === "all" || row["|k|"] === Number(selectedLength);
      const haystack = `${row.k} ${row.x} ${row.y} ${row.permutations}`.toLowerCase();
      const matchesQuery = !query || haystack.includes(query);
      return matchesLength && matchesQuery;
    });

    const visible = filtered.slice(0, limit);
    summary.text(`${formatInt(filtered.length)} matching rows. Showing ${formatInt(visible.length)}.`);

    tableBody
      .selectAll("tr")
      .data(visible, (d) => d.k)
      .join("tr")
      .html(
        (d) => `
          <td>${d.k}</td>
          <td>${d.x}</td>
          <td>${d.y}</td>
          <td>${formatInt(d["|permutations|"])}</td>
          <td>${formatInt(d.position_of_k)}</td>
          <td>${formatDepth(d.relative_depth)}</td>
          <td>${formatRatio(d.expansion_ratio)}</td>
        `
      );
  }

  searchInput.addEventListener("input", updateTable);
  lengthFilter.addEventListener("change", updateTable);
  limitFilter.addEventListener("change", updateTable);
  updateTable();
}

function showTooltip(event, html) {
  tooltip
    .style("opacity", 1)
    .html(html)
    .style("left", `${event.clientX + 14}px`)
    .style("top", `${event.clientY + 14}px`);
}

function hideTooltip() {
  tooltip.style("opacity", 0);
}
