/* Skip artifact shell — fixed helpers served beside every artifact. */
(function () {
  "use strict";

  var fmt = {
    num: function (v, opts) { return new Intl.NumberFormat("pt-BR", opts || {}).format(v); },
    brl: function (v) { return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(v); },
    pct: function (v) { return new Intl.NumberFormat("pt-BR", { style: "percent", maximumFractionDigits: 1 }).format(v); },
    compact: function (v) { return new Intl.NumberFormat("pt-BR", { notation: "compact", maximumFractionDigits: 1 }).format(v); },
    brlCompact: function (v) { return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", notation: "compact", maximumFractionDigits: 1 }).format(v); }
  };

  // axisLabels formats the five y-axis ticks in the unit the chart declared
  // (percent, BRL or plain numbers), compact so long values never clip, with
  // the fewest decimals that still print every tick exactly (1,5 mi, not 2 mi).
  function axisLabels(format, ticks) {
    function at(digits) {
      var opts = { notation: "compact", maximumFractionDigits: digits };
      if (format === "pct") opts = { style: "percent", maximumFractionDigits: digits };
      else if (format === "brl") opts = { style: "currency", currency: "BRL", notation: "compact", maximumFractionDigits: digits };
      var nf = new Intl.NumberFormat("pt-BR", opts);
      return ticks.map(function (t) { return nf.format(t); });
    }
    for (var digits = 0; digits < 2; digits++) {
      if (at(digits).join("|") === at(digits + 1).join("|")) return at(digits);
    }
    return at(2);
  }

  // yAxisPad formats the ticks and measures the left padding they need from
  // the longest one; drawYAxis then draws the grid and the labels.
  function yAxisPad(format, max) {
    var labels = axisLabels(format, [0, max / 4, max / 2, (max * 3) / 4, max]);
    var longest = labels.reduce(function (m, l) { return Math.max(m, l.length); }, 0);
    return { labels: labels, padL: Math.max(40, Math.round(longest * 6.2) + 14) };
  }
  function drawYAxis(svg, axis, W, padR, padT, plotH) {
    for (var g = 0; g <= 4; g++) {
      var gy = padT + plotH - (plotH * g) / 4;
      svg.appendChild(svgEl("line", { x1: axis.padL, y1: gy, x2: W - padR, y2: gy, stroke: "currentColor", "stroke-opacity": 0.08 }));
      var lbl = svgEl("text", { x: axis.padL - 8, y: gy + 4, "text-anchor": "end", "font-size": 10, fill: mutedColor() });
      lbl.textContent = axis.labels[g];
      svg.appendChild(lbl);
    }
  }

  // xLabelStep: show every k-th category label so labels never overlap, and
  // always the last one (counted back from the end).
  function xLabelStep(labels, step) {
    var longest = labels.reduce(function (m, l) { return Math.max(m, String(l).length); }, 0);
    return Math.max(1, Math.ceil((longest * 6.4 + 8) / Math.max(step, 1)));
  }
  function drawXLabel(svg, text, x, y, W, edgeGuard) {
    var anchor = "middle";
    var half = String(text).length * 3.2;
    if (edgeGuard && x - half < 4) anchor = "start";
    if (edgeGuard && x + half > W - 4) anchor = "end";
    var tx = svgEl("text", { x: x, y: y, "text-anchor": anchor, "font-size": 11, fill: mutedColor() });
    tx.textContent = text;
    svg.appendChild(tx);
  }
  // categoryLines fits a bar's category name in its slot: one line, two lines
  // split at a space, or cut with "…". A bar without its name can't be read, so
  // categories are never skipped; null when the slot is too narrow for that.
  function categoryLines(text, slot) {
    var fit = Math.floor((slot - 6) / 6.4);
    var s = String(text);
    if (fit < 4) return null;
    if (s.length <= fit) return [s];
    var cut = function (t) { return t.length <= fit ? t : t.slice(0, fit - 1).trimEnd() + "…"; };
    var best = -1;
    for (var i = 0; i < s.length; i++) {
      if (s[i] === " " && (best < 0 || Math.abs(s.length / 2 - i) < Math.abs(s.length / 2 - best))) best = i;
    }
    if (best < 0) return [cut(s)];
    return [cut(s.slice(0, best)), cut(s.slice(best + 1))];
  }
  function legend(el, items) {
    var box = document.createElement("div");
    box.className = "chart-legend";
    items.forEach(function (it) {
      var row = document.createElement("span");
      var dot = document.createElement("i");
      dot.style.background = it.color;
      row.appendChild(dot);
      row.appendChild(document.createTextNode((it.label || "") + (it.value ? " " : "")));
      if (it.value) {
        var v = document.createElement("b");
        v.textContent = it.value;
        row.appendChild(v);
      }
      box.appendChild(row);
    });
    resolve(el).appendChild(box);
  }
  var seriesPalette = ["#1baf7a", "#eda100", "#e34948", "#4a3aa7", "#e87ba4", "#0ea5b7"];

  // format accepts a function OR one of the fmt names ("num" | "brl" | "pct").
  // A page's function may return nothing or throw: the chart prints its
  // number instead of taking the rest of the page script down with it.
  function coerceFormat(spec) {
    if (typeof spec === "function") {
      return function (v) {
        try {
          var out = spec(v);
          return out == null ? "" : String(out);
        } catch (e) {
          return fmt.num(v);
        }
      };
    }
    if (typeof spec === "string" && fmt[spec]) return fmt[spec];
    return function (v) { return fmt.num(v); };
  }

  function accent() {
    return getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#2563eb";
  }
  function mutedColor() {
    return getComputedStyle(document.documentElement).getPropertyValue("--text-muted").trim() || "#5b6472";
  }
  function svgEl(tag, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var k in attrs) el.setAttribute(k, attrs[k]);
    return el;
  }
  function frame(el, w, h) {
    var svg = svgEl("svg", { viewBox: "0 0 " + w + " " + h, role: "img" });
    el = resolve(el);
    el.innerHTML = "";
    el.appendChild(svg);
    return svg;
  }

  // maxOf guards the axis scale: empty values would give -Infinity (truthy,
  // so "|| 1" can't catch it) and a non-positive max would flip the chart.
  // finite reads a chart value as a number, 0 when it is not one (NaN,
  // Infinity, a stray string), so one bad value cannot blank the axis.
  function finite(v) {
    var n = +v;
    return isFinite(n) ? n : 0;
  }

  function maxOf(values) {
    var m = values.length ? Math.max.apply(null, values.map(finite)) : 0;
    return m > 0 ? m : 1;
  }

  // labelsFor pads or trims the category names to the n points drawn: pages
  // pass labels and values of different lengths, and one throw here loses
  // every section the page renders after the chart.
  function labelsFor(cfg, n) {
    var out = [];
    for (var i = 0; i < n; i++) out.push(cfg.labels && cfg.labels[i] != null ? String(cfg.labels[i]) : "");
    return out;
  }

  // niceMax rounds the scale up so the four grid steps land on round values
  // (1, 1.5, 2, 2.5, 3, 4, 5, 6 or 8 × 10^k) and the tick labels read exactly.
  function niceMax(max) {
    var raw = max / 4;
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var res = raw / mag;
    var steps = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10];
    var nice = steps.filter(function (s) { return s >= res - 1e-9; })[0];
    return nice * mag * 4;
  }

  // bar(el, {labels:[], values:[], color?, format?}) — vertical bar chart.
  function bar(el, cfg) {
    var W = 640, H = 280, padB = 30, padT = 12, padR = 12;
    var max = niceMax(maxOf(cfg.values));
    var axis = yAxisPad(cfg.format, max);
    var svg = frame(el, W, H);
    var n = cfg.values.length;
    var labels = labelsFor(cfg, n);
    var plotW = W - axis.padL - padR;
    var step = plotW / n, bw = Math.min(step * 0.62, 64);
    var names = labels.map(function (l) { return categoryLines(l, step); });
    var named = names.every(Boolean);
    if (named && names.some(function (l) { return l.length > 1; })) padB = 42;
    var plotH = H - padT - padB;
    var color = cfg.color || accent();
    var f = coerceFormat(cfg.format);
    var every = xLabelStep(labels, step);
    drawYAxis(svg, axis, W, padR, padT, plotH);
    cfg.values.forEach(function (v, i) {
      var bh = Math.max(0, (finite(v) / max) * plotH);
      var x = axis.padL + i * step + (step - bw) / 2;
      var y = padT + plotH - bh;
      var r = svgEl("rect", { x: x, y: y, width: bw, height: bh, rx: 4, fill: (cfg.colors && cfg.colors[i]) || color });
      var t = svgEl("title", {});
      t.textContent = labels[i] + ": " + f(v);
      r.appendChild(t);
      svg.appendChild(r);
      if (named) {
        names[i].forEach(function (text, li) {
          drawXLabel(svg, text, x + bw / 2, padT + plotH + 18 + li * 13, W, false);
        });
      } else if ((n - 1 - i) % every === 0) {
        drawXLabel(svg, labels[i], x + bw / 2, H - 10, W, false);
      }
    });
  }

  // line(el, {labels:[], values:[] | series:[{label, values, color?}], color?, format?})
  // — one line, or several series on one scale with a legend under the chart.
  function line(el, cfg) {
    var W = 640, H = 280, padB = 30, padT = 12, padR = 16;
    var series = cfg.series && cfg.series.length
      ? cfg.series
      : [{ label: "", values: cfg.values || [], color: cfg.color }];
    var all = [];
    series.forEach(function (s) { all = all.concat(s.values || []); });
    var max = niceMax(maxOf(all));
    var axis = yAxisPad(cfg.format, max);
    var svg = frame(el, W, H);
    var n = series.reduce(function (m, s) { return Math.max(m, (s.values || []).length); }, 0);
    var labels = labelsFor(cfg, n);
    var plotW = W - axis.padL - padR, plotH = H - padT - padB;
    var f = coerceFormat(cfg.format);
    drawYAxis(svg, axis, W, padR, padT, plotH);
    var xs = labels.map(function (_, i) { return axis.padL + (n === 1 ? plotW / 2 : (plotW * i) / (n - 1)); });
    var every = xLabelStep(labels, n > 1 ? plotW / (n - 1) : plotW);
    labels.forEach(function (label, i) {
      if ((n - 1 - i) % every === 0) drawXLabel(svg, label, xs[i], H - 10, W, true);
    });
    var colors = series.map(function (s, si) {
      return s.color || (si === 0 ? (cfg.color || accent()) : seriesPalette[(si - 1) % seriesPalette.length]);
    });
    series.forEach(function (s, si) {
      var color = colors[si];
      var pts = (s.values || []).map(function (v, i) { return [xs[i], padT + plotH - (finite(v) / max) * plotH]; });
      var d = pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join(" ");
      svg.appendChild(svgEl("path", { d: d, fill: "none", stroke: color, "stroke-width": 2, "stroke-linejoin": "round" }));
      pts.forEach(function (p, i) {
        var c = svgEl("circle", { cx: p[0], cy: p[1], r: 3.5, fill: color });
        var t = svgEl("title", {});
        t.textContent = (s.label ? s.label + " · " : "") + labels[i] + ": " + f(s.values[i]);
        c.appendChild(t);
        svg.appendChild(c);
      });
    });
    if (series.length > 1) {
      legend(el, series.map(function (s, si) { return { label: s.label, color: colors[si] }; }));
    }
  }

  // donut(el, {labels:[], values:[], colors?, format?, center?, centerLabel?, legend?})
  // — donut with a short total in the centre (compact, in the declared unit)
  // and, with legend: true, the labels and shares listed under it.
  function donut(el, cfg) {
    var W = 320, H = 280, cx = W / 2, cy = H / 2, R = 92, r = 58;
    var svg = frame(el, W, H);
    // At 100% of a wide container the donut outgrows the height pages give
    // the box and spills over the next section: keep it at its own size.
    svg.style.maxWidth = W + "px";
    svg.style.margin = "0 auto";
    var values = cfg.values.map(finite);
    var labels = labelsFor(cfg, values.length);
    var sum = values.reduce(function (a, b) { return a + b; }, 0);
    var total = sum || 1;
    var palette = cfg.colors || [accent()].concat(seriesPalette);
    // The hover keeps the full value; the centre has room for a short one.
    var full = coerceFormat(cfg.format);
    var short = typeof cfg.format === "function" ? full : cfg.format === "brl" ? fmt.brlCompact : fmt.compact;
    var a0 = -Math.PI / 2;
    values.forEach(function (v, i) {
      var a1 = a0 + (v / total) * Math.PI * 2;
      var large = a1 - a0 > Math.PI ? 1 : 0;
      var p = ["M", cx + R * Math.cos(a0), cy + R * Math.sin(a0),
        "A", R, R, 0, large, 1, cx + R * Math.cos(a1), cy + R * Math.sin(a1),
        "L", cx + r * Math.cos(a1), cy + r * Math.sin(a1),
        "A", r, r, 0, large, 0, cx + r * Math.cos(a0), cy + r * Math.sin(a0), "Z"].join(" ");
      var path = svgEl("path", { d: p, fill: palette[i % palette.length] });
      var t = svgEl("title", {});
      t.textContent = labels[i] + ": " + full(v) + " (" + fmt.pct(v / total) + ")";
      path.appendChild(t);
      svg.appendChild(path);
      a0 = a1;
    });
    // A share chart has no total worth printing: without its own centre text
    // the caption alone takes the middle.
    var text = cfg.center != null ? String(cfg.center) : (cfg.format === "pct" ? "" : short(sum));
    if (text) {
      var size = text.length > 9 ? 14 : text.length > 7 ? 17 : 20;
      var center = svgEl("text", { x: cx, y: cfg.centerLabel ? cy + 1 : cy + 6, "text-anchor": "middle", "font-size": size, "font-weight": 650, fill: "currentColor" });
      center.textContent = text;
      svg.appendChild(center);
    }
    if (cfg.centerLabel) {
      var cap = svgEl("text", { x: cx, y: text ? cy + 19 : cy + 5, "text-anchor": "middle", "font-size": 11, fill: mutedColor() });
      cap.textContent = cfg.centerLabel;
      svg.appendChild(cap);
    }
    if (cfg.legend) {
      legend(el, labels.map(function (label, i) {
        return { label: label, color: palette[i % palette.length], value: fmt.pct(values[i] / total) };
      }));
    }
  }

  // ---- Page building blocks: what dashboards and small systems kept
  // re-implementing — a searchable sortable table, a KPI row, tabs, toasts,
  // dialogs, saved state and mock data. Every call is opt-in, so a page that
  // brings its own versions keeps them.

  function resolve(target) {
    return typeof target === "string" ? document.querySelector(target) : target;
  }

  function node(tag, className, text) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (text != null) el.textContent = text;
    return el;
  }

  function isNumberColumn(col) {
    return col.align === "right" || col.format === "num" || col.format === "brl" || col.format === "pct";
  }

  function cellText(col, row) {
    var value = row[col.key];
    if (value == null) return "";
    return col.format ? coerceFormat(col.format)(value) : String(value);
  }

  function compareValues(a, b) {
    if (typeof a === "number" && typeof b === "number") return a - b;
    return String(a == null ? "" : a).localeCompare(String(b == null ? "" : b), "pt-BR", { numeric: true });
  }

  // table(el, {columns, rows, search?, pageSize?, empty?, onRowClick?}) — a
  // table.shell-table with sortable headers, an optional search box and
  // pager. A column is {key, label, format?, align?, sortable? (true),
  // render?(value, row) returning a Node or an HTML string — the page writes
  // its cell templates as markup}. Plain values are always set as text.
  // Returns {setRows, rows}.
  function table(target, cfg) {
    var root = resolve(target);
    var cols = cfg.columns || [];
    var pageSize = cfg.pageSize || 0;
    var state = { rows: (cfg.rows || []).slice(), query: "", key: null, dir: 1, page: 0 };
    root.innerHTML = "";
    if (cfg.search) {
      var search = node("input", "input skip-table-search");
      search.type = "search";
      search.placeholder = typeof cfg.search === "string" ? cfg.search : "Buscar…";
      search.setAttribute("aria-label", search.placeholder);
      search.addEventListener("input", function () {
        state.query = search.value.trim().toLowerCase();
        state.page = 0;
        draw();
      });
      root.appendChild(search);
    }
    var tableEl = node("table", "shell-table");
    var headRow = node("tr");
    var heads = cols.map(function (col) {
      var th = node("th", isNumberColumn(col) ? "num" : "", col.label == null ? col.key : col.label);
      th.scope = "col";
      if (col.sortable !== false) {
        var toggle = function () {
          state.dir = state.key === col.key ? -state.dir : 1;
          state.key = col.key;
          draw();
        };
        th.setAttribute("data-sort", col.key);
        th.tabIndex = 0;
        th.addEventListener("click", toggle);
        th.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
        });
      }
      headRow.appendChild(th);
      return th;
    });
    var thead = node("thead");
    var tbody = node("tbody");
    var wrap = node("div", "skip-table-wrap");
    var pager = node("div", "skip-pager");
    thead.appendChild(headRow);
    tableEl.appendChild(thead);
    tableEl.appendChild(tbody);
    wrap.appendChild(tableEl);
    root.appendChild(wrap);
    if (pageSize) root.appendChild(pager);

    function visibleRows() {
      var rows = state.rows;
      if (state.query) {
        rows = rows.filter(function (row) {
          return cols.some(function (col) { return cellText(col, row).toLowerCase().indexOf(state.query) >= 0; });
        });
      }
      if (state.key) {
        var key = state.key, dir = state.dir;
        rows = rows.slice().sort(function (a, b) { return dir * compareValues(a[key], b[key]); });
      }
      return rows;
    }

    function drawRow(row) {
      var tr = node("tr");
      cols.forEach(function (col) {
        var td = node("td", isNumberColumn(col) ? "num" : "");
        if (!col.render) {
          td.textContent = cellText(col, row);
        } else {
          var content = col.render(row[col.key], row);
          if (content instanceof Node) td.appendChild(content);
          else td.innerHTML = content == null ? "" : String(content);
        }
        tr.appendChild(td);
      });
      // The row stays a row (no role) and takes focus, so a keyboard reaches
      // the same action; keys pressed on a control inside a cell are its own.
      if (cfg.onRowClick) {
        tr.style.cursor = "pointer";
        tr.tabIndex = 0;
        tr.addEventListener("click", function () { cfg.onRowClick(row); });
        tr.addEventListener("keydown", function (e) {
          if (e.target !== tr || (e.key !== "Enter" && e.key !== " ")) return;
          e.preventDefault();
          cfg.onRowClick(row);
        });
      }
      return tr;
    }

    function pagerButton(label, disabled, step) {
      var button = node("button", "btn", label);
      button.type = "button";
      button.setAttribute("data-variant", "outline");
      button.setAttribute("data-size", "sm");
      button.disabled = disabled;
      button.addEventListener("click", function () { state.page += step; draw(); });
      return button;
    }

    function draw() {
      var rows = visibleRows();
      heads.forEach(function (th, i) {
        if (cols[i].key === state.key) th.setAttribute("aria-sort", state.dir > 0 ? "ascending" : "descending");
        else th.removeAttribute("aria-sort");
      });
      var pages = pageSize ? Math.max(1, Math.ceil(rows.length / pageSize)) : 1;
      state.page = Math.min(state.page, pages - 1);
      var shown = pageSize ? rows.slice(state.page * pageSize, (state.page + 1) * pageSize) : rows;
      tbody.innerHTML = "";
      if (!shown.length) {
        var empty = node("td", "skip-table-empty", cfg.empty || "Nenhum registro encontrado.");
        empty.colSpan = cols.length;
        tbody.appendChild(node("tr")).appendChild(empty);
      }
      shown.forEach(function (row) { tbody.appendChild(drawRow(row)); });
      if (!pageSize) return;
      pager.innerHTML = "";
      var from = rows.length ? state.page * pageSize + 1 : 0;
      pager.appendChild(node("span", "", from + "–" + Math.min(rows.length, (state.page + 1) * pageSize) + " de " + rows.length));
      var nav = node("div", "row gap-2");
      nav.appendChild(pagerButton("Anterior", state.page === 0, -1));
      nav.appendChild(pagerButton("Próxima", state.page >= pages - 1, 1));
      pager.appendChild(nav);
    }

    draw();
    return {
      setRows: function (rows) { state.rows = rows.slice(); draw(); },
      rows: visibleRows
    };
  }

  // kpis(el, [{label, value, format?, delta?, hint?}]) — KPI cards in a
  // responsive grid; delta is a fraction (0.12 renders as ▲ 12%).
  function kpis(target, items) {
    var root = resolve(target);
    root.innerHTML = "";
    root.classList.add("shell-grid");
    items.forEach(function (item) {
      var card = node("div", "panel kpi");
      card.appendChild(node("span", "kpi-label", item.label));
      // Large money values go compact ("R$ 27,5 mi"): the full amount does
      // not fit a KPI card at four per row.
      var kpiFormat = item.format === "brl" && Math.abs(item.value) >= 1e6 ? fmt.brlCompact : (item.format ? coerceFormat(item.format) : null);
      card.appendChild(node("span", "kpi-value", kpiFormat ? kpiFormat(item.value) : String(item.value)));
      if (typeof item.delta === "number") {
        var up = item.delta >= 0;
        card.appendChild(node("span", "kpi-delta " + (up ? "up" : "down"), (up ? "▲ " : "▼ ") + fmt.pct(Math.abs(item.delta))));
      }
      if (item.hint) card.appendChild(node("span", "kpi-label", item.hint));
      root.appendChild(card);
    });
  }

  // badge(text, variant?) — a .badge node for table cells and lists;
  // variant is "secondary" | "outline" | "destructive" (default: primary).
  function badge(text, variant) {
    var el = node("span", "badge", text);
    if (variant) el.setAttribute("data-variant", variant);
    return el;
  }

  // tabs(el) — wires one .tabs block: [role=tab] buttons inside
  // [role=tablist], each with aria-controls naming its [role=tabpanel].
  function tabs(target) {
    var root = resolve(target);
    var buttons = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function select(chosen) {
      buttons.forEach(function (b) {
        var on = b === chosen;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(b.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
    }
    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () { select(b); });
      b.addEventListener("keydown", function (e) {
        var step = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!step) return;
        var next = buttons[(i + step + buttons.length) % buttons.length];
        next.focus();
        select(next);
      });
    });
    select(buttons.filter(function (b) { return b.getAttribute("aria-selected") === "true"; })[0] || buttons[0]);
  }

  // toast(message, {type?: "success" | "error", title?, duration?}) — a
  // .toast in a shared .toaster at the bottom of the page.
  function toast(message, opts) {
    opts = opts || {};
    var toaster = document.querySelector(".toaster") || document.body.appendChild(node("div", "toaster"));
    var item = node("div", "toast");
    item.setAttribute("role", opts.type === "error" ? "alert" : "status");
    item.setAttribute("aria-hidden", "true");
    if (opts.type) item.setAttribute("data-type", opts.type);
    var content = node("div", "toast-content");
    var section = node("section");
    if (opts.title) section.appendChild(node("h2", "", opts.title));
    section.appendChild(node("p", "", message));
    content.appendChild(section);
    item.appendChild(content);
    toaster.appendChild(item);
    requestAnimationFrame(function () { item.setAttribute("aria-hidden", "false"); });
    setTimeout(function () {
      item.setAttribute("aria-hidden", "true");
      setTimeout(function () { item.remove(); }, 400);
    }, opts.duration || 3000);
  }

  // Dialogs are native <dialog class="dialog">: a [data-dialog-open="id"]
  // anywhere opens one, a [data-dialog-close] inside closes it, and a click on
  // its backdrop closes it too. Plain dialog.showModal()/close() still work.
  document.addEventListener("click", function (e) {
    var target = e.target;
    if (!(target instanceof Element)) return;
    var opener = target.closest("[data-dialog-open]");
    if (opener) {
      var dialog = document.getElementById(opener.getAttribute("data-dialog-open"));
      if (dialog && dialog.showModal && !dialog.open) dialog.showModal();
      return;
    }
    var closer = target.closest("[data-dialog-close]");
    if (closer && closer.closest("dialog")) {
      closer.closest("dialog").close();
      return;
    }
    if (target.tagName === "DIALOG" && target.classList.contains("dialog") && target.open) target.close();
  });

  // store(key, fallback) — JSON state in localStorage that never throws (a
  // private window or a full quota falls back to memory): {get, set, update}.
  function store(key, fallback) {
    var memory;
    // Set while the last write did not reach localStorage: what is stored
    // there is older than memory until a write goes through again.
    var unsaved = false;
    var initial = function () { return fallback === undefined ? undefined : JSON.parse(JSON.stringify(fallback)); };
    function get() {
      if (!unsaved) {
        try {
          var raw = localStorage.getItem(key);
          if (raw != null) return JSON.parse(raw);
        } catch (e) { /* storage unavailable: memory below */ }
      }
      return memory !== undefined ? memory : initial();
    }
    function set(value) {
      memory = value;
      try {
        localStorage.setItem(key, JSON.stringify(value));
        unsaved = false;
      } catch (e) {
        unsaved = true;
      }
      return value;
    }
    return { get: get, set: set, update: function (fn) { return set(fn(get())); } };
  }

  // mock — seeded random data, so a page asks for 90 days of numbers in one
  // line instead of writing them out; the same seed gives the same data.
  var FIRST = ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela", "Henrique", "Isabela", "João",
    "Larissa", "Marcos", "Natália", "Otávio", "Paula", "Rafael", "Sofia", "Thiago", "Vanessa", "Lucas"];
  var LAST = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento", "Lima",
    "Araújo", "Fernandes", "Carvalho", "Gomes", "Martins", "Rocha", "Ribeiro", "Barbosa"];
  var INITIALS = "ABCDEFGHIJLMNOPRSTV".split("");
  var CITIES = ["São Paulo, SP", "Rio de Janeiro, RJ", "Belo Horizonte, MG", "Curitiba, PR", "Porto Alegre, RS",
    "Salvador, BA", "Recife, PE", "Fortaleza, CE", "Brasília, DF", "Goiânia, GO", "Campinas, SP", "Florianópolis, SC",
    "Manaus, AM", "Belém, PA", "Vitória, ES", "Natal, RN"];

  function createMock(seed) {
    var state = seed >>> 0;
    var names = 0;
    function random() {
      state = (state + 0x6d2b79f5) >>> 0;
      var t = state;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
    function int(min, max) { return min + Math.floor(random() * (max - min + 1)); }
    function pick(list) { return list[Math.floor(random() * list.length)]; }
    var mock = {
      seed: function (value) { state = value >>> 0; names = 0; return mock; },
      random: random,
      int: int,
      float: function (min, max, decimals) {
        var factor = Math.pow(10, decimals == null ? 2 : decimals);
        return Math.round((min + random() * (max - min)) * factor) / factor;
      },
      pick: pick,
      chance: function (p) { return random() < p; },
      // There are 360 first/last pairs. A page that draws until the name is
      // new (do { … } while (used.has(name))) froze the tab past them, so
      // later draws widen the space: a second surname after 200 (6,480), a
      // middle initial after 4,000.
      name: function () {
        names++;
        var middle = names > 4000 ? pick(INITIALS) + ". " : "";
        return pick(FIRST) + " " + middle + (names > 200 ? pick(LAST) + " " : "") + pick(LAST);
      },
      city: function () { return pick(CITIES); },
      // series(n, {start, trend, noise, min, decimals}) — a walk: each value
      // moves by trend (fraction per step) plus up to ±noise of itself.
      series: function (n, opts) {
        opts = opts || {};
        var value = opts.start == null ? 100 : opts.start;
        var factor = Math.pow(10, opts.decimals || 0);
        var out = [];
        for (var i = 0; i < n; i++) {
          out.push(Math.max(opts.min == null ? 0 : opts.min, Math.round(value * factor) / factor));
          value = value * (1 + (opts.trend || 0)) * (1 + (random() * 2 - 1) * (opts.noise == null ? 0.08 : opts.noise));
        }
        return out;
      },
      // dates(n, {end?, step?: "day" | "week" | "month"}) — ISO dates
      // (YYYY-MM-DD), oldest first, ending at end (default: today).
      dates: function (n, opts) {
        opts = opts || {};
        var end = opts.end ? new Date(opts.end) : new Date();
        var out = [];
        for (var i = n - 1; i >= 0; i--) {
          var d = new Date(end.getTime());
          if (opts.step === "month") d.setMonth(d.getMonth() - i);
          else d.setDate(d.getDate() - i * (opts.step === "week" ? 7 : 1));
          out.push(d.toISOString().slice(0, 10));
        }
        return out;
      },
      // rows(n, spec) — n objects; each spec value is a function(i), a list
      // to pick from, or a constant.
      rows: function (n, spec) {
        var out = [];
        for (var i = 0; i < n; i++) {
          var row = {};
          for (var key in spec) {
            var value = spec[key];
            row[key] = typeof value === "function" ? value(i) : Array.isArray(value) ? pick(value) : value;
          }
          out.push(row);
        }
        return out;
      }
    };
    return mock;
  }

  window.skipShell = { fmt: fmt };
  window.skipChart = { bar: bar, line: line, donut: donut };
  window.skipUI = { table: table, kpis: kpis, badge: badge, tabs: tabs, toast: toast };
  window.skipStore = store;
  window.skipMock = createMock(20261022);
})();
