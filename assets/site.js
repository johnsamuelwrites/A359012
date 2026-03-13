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
      }))
      .sort((a, b) => d3.ascending(a.k, b.k));

    renderHeroStats(data);
    renderMetrics(data);
    renderLengthChart(data);
    renderSplitHeatmap(data);
    renderGrowthChart(data);
    renderScatterPlot(data);
    renderDepthHistogram(data);
    renderLogLogGrowth(data);
    renderGapChart(data);
    renderTable(data);
  })
  .catch((error) => {
    console.error(error);
    d3.select("#dashboard")
      .append("p")
      .text("Unable to load A359012.csv. Serve the project through a local web server so D3 can fetch the dataset.");
  });

function renderHeroStats(data) {
  const uniqueK = [...new Set(data.map((d) => d.k))];
  const primeCount = data.filter((d) => d.is_prime === 1).length;
  const stats = [
    { label: "Terms (unique k)", value: formatInt(uniqueK.length) },
    { label: "Max k", value: formatInt(d3.max(data, (d) => d.k)) },
    { label: "Longest witness", value: formatInt(d3.max(data, (d) => d["|permutations|"])) + " digits" },
    { label: "Prime terms", value: formatInt(primeCount) },
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
  const multiWitness = [...new Set(data.filter((d) => d.num_witnesses > 1).map((d) => d.k))];
  const nonTZTerms = data.filter((d) => d.trailing_zero === 0);
  const gaps = data
    .filter((d) => d.gap_prev > 0)
    .map((d) => d.gap_prev);
  const maxGap = gaps.length ? d3.max(gaps) : 0;
  const metrics = [
    {
      label: "Trailing-zero witnesses",
      value: `${formatInt(data.filter((d) => d.trailing_zero === 1).length)}/${formatInt(data.length)}`,
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
    {
      label: "Non-trailing-zero outliers",
      value: formatInt(nonTZTerms.length),
      detail: nonTZTerms.map((d) => `k=${d.k} (P(${d.x},${d.y}) ends in ${String(d.permutations).slice(-1)})`).join("; ") || "None",
    },
    {
      label: "Multiple-witness terms",
      value: multiWitness.length ? multiWitness.join(", ") : "None found",
      detail: "Terms where two different (x, y) splits both produce a valid witness.",
    },
    {
      label: "Largest inter-term gap",
      value: formatInt(maxGap),
      detail: "The widest stretch of consecutive integers containing no sequence terms.",
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
  const filterPrime = document.getElementById("filter-prime");
  const filterPalindrome = document.getElementById("filter-palindrome");
  const filterDistinct = document.getElementById("filter-distinct");
  const filterNonzero = document.getElementById("filter-nonzero");
  const filterMulti = document.getElementById("filter-multi");
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
      const matchesPrime = !filterPrime.checked || row.is_prime === 1;
      const matchesPalindrome = !filterPalindrome.checked || row.palindrome;
      const matchesDistinct = !filterDistinct.checked || !row.repeatedDigits;
      const matchesNonzero = !filterNonzero.checked || row.trailing_zero === 0;
      const matchesMulti = !filterMulti.checked || row.num_witnesses > 1;
      return matchesLength && matchesQuery && matchesPrime && matchesPalindrome
        && matchesDistinct && matchesNonzero && matchesMulti;
    });

    const visible = filtered.slice(0, limit);
    summary.text(`${formatInt(filtered.length)} matching rows. Showing ${formatInt(visible.length)}.`);

    tableBody
      .selectAll("tr")
      .data(visible, (d) => `${d.k}-${d.x}-${d.y}`)
      .join("tr")
      .html(
        (d) => `
          <td>${d.k}${d.is_prime ? ' <span class="badge-prime" title="prime">★</span>' : ""}${d.palindrome ? ' <span class="badge-palindrome" title="palindrome">⬡</span>' : ""}</td>
          <td>${d.x}</td>
          <td>${d.y}</td>
          <td>${formatInt(d["|permutations|"])}</td>
          <td>${formatInt(d.position_of_k)}</td>
          <td>${formatDepth(d.relative_depth)}</td>
          <td>${formatRatio(d.expansion_ratio)}</td>
          <td>${d.digit_sum}</td>
          <td>${d.num_witnesses > 1 ? `<strong>${d.num_witnesses}</strong>` : d.num_witnesses}</td>
        `
      );
  }

  searchInput.addEventListener("input", updateTable);
  lengthFilter.addEventListener("change", updateTable);
  limitFilter.addEventListener("change", updateTable);
  filterPrime.addEventListener("change", updateTable);
  filterPalindrome.addEventListener("change", updateTable);
  filterDistinct.addEventListener("change", updateTable);
  filterNonzero.addEventListener("change", updateTable);
  filterMulti.addEventListener("change", updateTable);
  updateTable();
}

function renderDepthHistogram(data) {
  const numBins = 10;
  const bins = d3.range(numBins).map((i) => ({
    label: `${(i / numBins).toFixed(1)}–${((i + 1) / numBins).toFixed(1)}`,
    lo: i / numBins,
    hi: (i + 1) / numBins,
    count: 0,
  }));
  data.forEach((d) => {
    const b = Math.min(Math.floor(d.relative_depth * numBins), numBins - 1);
    bins[b].count += 1;
  });

  const container = d3.select("#depth-histogram");
  const width = container.node().clientWidth || 540;
  const height = 340;
  const margin = { top: 16, right: 18, bottom: 52, left: 52 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleBand()
    .domain(bins.map((b) => b.label))
    .range([margin.left, width - margin.right])
    .padding(0.18);
  const y = d3.scaleLinear()
    .domain([0, d3.max(bins, (b) => b.count)])
    .nice()
    .range([height - margin.bottom, margin.top]);

  // Uniform reference line
  const uniform = data.length / numBins;
  svg.append("line")
    .attr("x1", margin.left).attr("x2", width - margin.right)
    .attr("y1", y(uniform)).attr("y2", y(uniform))
    .attr("stroke", colors.muted)
    .attr("stroke-dasharray", "5,4")
    .attr("stroke-width", 1.5);

  svg.append("g").attr("class", "grid").attr("transform", "translate(0,0)")
    .call(d3.axisLeft(y).ticks(5).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .select(".domain").remove();

  svg.selectAll(".bar")
    .data(bins)
    .join("rect")
    .attr("x", (b) => x(b.label))
    .attr("y", (b) => y(b.count))
    .attr("width", x.bandwidth())
    .attr("height", (b) => y(0) - y(b.count))
    .attr("rx", 10)
    .attr("fill", colors.accent2)
    .attr("fill-opacity", 0.82)
    .on("mousemove", (event, b) =>
      showTooltip(event, `Depth ${b.label}<br><strong>${formatInt(b.count)} terms</strong>`)
    )
    .on("mouseleave", hideTooltip);

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSize(0))
    .selectAll("text").attr("transform", "rotate(-35)").style("text-anchor", "end");

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5));

  svg.append("text").attr("class", "chart-label")
    .attr("x", width / 2).attr("y", height - 4)
    .attr("text-anchor", "middle").text("Relative depth bin");
}

function renderLogLogGrowth(data) {
  // Build cumulative count over unique k values
  const uniqueKSorted = [...new Set(data.map((d) => d.k))].sort(d3.ascending);
  const growth = uniqueKSorted.map((k, i) => ({ k, count: i + 1 }));

  const container = d3.select("#loglog-chart");
  const width = container.node().clientWidth || 540;
  const height = 340;
  const margin = { top: 18, right: 18, bottom: 46, left: 62 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleLog().domain(d3.extent(growth, (d) => d.k)).range([margin.left, width - margin.right]);
  const y = d3.scaleLog().domain([1, d3.max(growth, (d) => d.count)]).range([height - margin.bottom, margin.top]);

  // Power-law reference line: fit slope from first and last point
  const x0 = growth[0].k, y0 = growth[0].count;
  const x1 = growth[growth.length - 1].k, y1 = growth[growth.length - 1].count;
  const alpha = Math.log(y1 / y0) / Math.log(x1 / x0);
  const C = y0 / Math.pow(x0, alpha);
  const refLine = [{ k: x0 }, { k: x1 }].map((d) => ({ k: d.k, count: C * Math.pow(d.k, alpha) }));

  svg.append("g").attr("class", "grid").attr("transform", "translate(0,0)")
    .call(d3.axisLeft(y).ticks(4).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .select(".domain").remove();

  const refPath = d3.line().x((d) => x(d.k)).y((d) => y(d.count));
  svg.append("path").datum(refLine)
    .attr("fill", "none").attr("stroke", colors.accent3)
    .attr("stroke-width", 1.5).attr("stroke-dasharray", "6,4")
    .attr("d", refPath);

  const linePath = d3.line().x((d) => x(d.k)).y((d) => y(d.count)).curve(d3.curveMonotoneX);
  svg.append("path").datum(growth)
    .attr("fill", "none").attr("stroke", colors.accent).attr("stroke-width", 2.5)
    .attr("d", linePath);

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(4, "~s"));

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(4, "~s"));

  svg.append("text").attr("class", "chart-label")
    .attr("x", width / 2).attr("y", height - 6)
    .attr("text-anchor", "middle").text("k (log scale)");

  svg.append("text").attr("class", "chart-label")
    .attr("transform", `translate(14 ${height / 2}) rotate(-90)`)
    .attr("text-anchor", "middle").text("Count (log scale)");

  svg.append("text")
    .attr("x", width - margin.right - 4).attr("y", margin.top + 14)
    .attr("text-anchor", "end").attr("fill", colors.accent3)
    .style("font-size", "11px")
    .text(`α ≈ ${alpha.toFixed(3)}`);
}

function renderGapChart(data) {
  // Get unique (k, gap_prev) — deduplicate by k
  const seen = new Set();
  const gapData = [];
  data.forEach((d) => {
    if (!seen.has(d.k)) {
      seen.add(d.k);
      if (d.gap_prev > 0) gapData.push({ k: d.k, gap: d.gap_prev });
    }
  });

  const container = d3.select("#gap-chart");
  const width = container.node().clientWidth || 920;
  const height = 520;
  const margin = { top: 18, right: 18, bottom: 50, left: 62 };

  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const x = d3.scaleLinear().domain(d3.extent(gapData, (d) => d.k)).range([margin.left, width - margin.right]);
  const y = d3.scaleLinear().domain([0, d3.max(gapData, (d) => d.gap)]).nice().range([height - margin.bottom, margin.top]);

  svg.append("g").attr("class", "grid").attr("transform", "translate(0,0)")
    .call(d3.axisLeft(y).ticks(5).tickSize(-(width - margin.left - margin.right)).tickFormat(""))
    .select(".domain").remove();

  svg.selectAll(".gap-bar")
    .data(gapData)
    .join("line")
    .attr("x1", (d) => x(d.k)).attr("x2", (d) => x(d.k))
    .attr("y1", y(0)).attr("y2", (d) => y(d.gap))
    .attr("stroke", (d) => d.gap > 500 ? colors.accent3 : colors.accent2)
    .attr("stroke-width", 1.5)
    .attr("stroke-opacity", 0.7)
    .on("mousemove", (event, d) =>
      showTooltip(event, `k = ${formatInt(d.k)}<br>Gap from previous: <strong>${formatInt(d.gap)}</strong>`)
    )
    .on("mouseleave", hideTooltip);

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(6).tickFormat(formatInt));

  svg.append("g").attr("class", "axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5));

  svg.append("text").attr("class", "chart-label")
    .attr("x", width / 2).attr("y", height - 10)
    .attr("text-anchor", "middle").text("k");

  svg.append("text").attr("class", "chart-label")
    .attr("transform", `translate(16 ${height / 2}) rotate(-90)`)
    .attr("text-anchor", "middle").text("Gap from previous term");
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
