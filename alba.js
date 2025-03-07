function older_or_equal(v1, v2) {
  return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] <= v2[2])));
}
function older(v1, v2) {
  return v1[0] < v2[0] || (v1[0] == v2[0] && (v1[1] < v2[1] || (v1[1] == v2[1] && v1[2] < v2[2])));
}
function show_version_diff(version) {
  chosen_oldest = null;
  for (var input of document.querySelectorAll('input[name="oldest"]')) {
    if (input.name != "oldest") {
      continue;
    }
    input_version = input.value.split("-").map(x => parseInt(x));
    chosen_oldest_version = chosen_oldest?.value.split("-").map(x => parseInt(x));
    if (older(input_version, version.split("-").map(x => parseInt(x))) &&
      (chosen_oldest_version == null || older(chosen_oldest_version, input_version))) {
      chosen_oldest = input;
    }
  }
  if (!chosen_oldest) {
    chosen_oldest = document.querySelector('input[name="oldest"][value="' + version + '"]')
  }
  chosen_oldest.checked = true;
  document.querySelector('input[name="newest"][value="' + version + '"]').checked = true;
  meow();
}

function update_from_query() {
  params = (new URL(document.location)).searchParams;
  if (params.has("v")) {
    const v = params.get("v").replaceAll(".", "-");
    document.querySelector('input[name="newest"][value="' + v + '"]').checked = true
    if (params.has("base")) {
      document.querySelector('input[name="oldest"][value="' + params.get("base").replaceAll(".", "-") + '"]').checked = true
    } else {
      document.querySelector('input[name="oldest"][value="' + v + '"]').checked = true
    }
  }
  if (params.has("show_deleted")) {
    document.querySelector('input[name="show-deleted"]').checked = params.get("show_deleted") === "true";
  }
  meow(false);
}

function meow(push_history = true) {
  oldest = document.querySelector('input[name="oldest"]:checked').value.split("-").map(x => parseInt(x));
  newest = document.querySelector('input[name="newest"]:checked').value.split("-").map(x => parseInt(x));
  show_deleted_paragraphs = document.querySelector('input[name="show-deleted"]').checked;
  if (push_history) {
    let query = [`v=${newest.join(".")}`];
    if (older(oldest, newest)) {
      query.push(`base=${oldest.join(".")}`);
    }
    if (show_deleted_paragraphs) {
      query.push(`show_deleted=${show_deleted_paragraphs}`);
    }
    var newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + query.join("&") + window.location.hash;
    window.history.pushState({ path: newurl }, '', newurl);
  }
  for (var label of document.getElementsByTagName("button")) {
    version = label.className.split("-").slice(-3).map(x => parseInt(x));
    if (older_or_equal(version, oldest)) {
      label.style = "color:black;background:white;";
    } else if (older(newest, version)) {
      label.style = "color:black;background:white;border:dashed";
    } else {
      label.style = "";
    }
  }
  for (var ins of document.getElementsByTagName("ins")) {
    version = ins.className.split("-").slice(-3).map(x => parseInt(x));
    if (older_or_equal(version, oldest)) {
      ins.style = "color:black;text-decoration:none;background-color:white;";
    } else if (older(newest, version)) {
      ins.style = "display:none";
    } else {
      ins.style = "";
    }
  }
  for (var table of document.querySelectorAll("table[class^=changed-in-]")) {
    version = table.className.split("-").slice(-3).map(x => parseInt(x));
    if (older_or_equal(version, oldest)) {
      table.style = "color:black;text-decoration:none;background-color:white;";
    } else if (older(newest, version)) {
      table.style = "display:none";
    } else {
      table.style = "";
    }
  }
  for (var del of document.getElementsByTagName("del")) {
    version = del.className.split("-").slice(-3).map(x => parseInt(x));
    if (older_or_equal(version, oldest)) {
      del.style = "display:none";
    } else if (older(newest, version)) {
      del.style = "text-decoration:none";
    } else if (del.classList.contains("paranum")) {
      del.style = "display:none";
    } else {
      del.style = "";
    }
  }
  for (var div of document.querySelectorAll("div.paragraph")) {
    version_added = null;
    version_removed = null;
    for (var c of div.classList) {
      if (c.startsWith("added-in-")) {
        version_added = c.split("-").slice(-3).map(x => parseInt(x));
      } else if (c.startsWith("removed-in-")) {
        version_removed = c.split("-").slice(-3).map(x => parseInt(x));
      }
    }
    if (version_added && older(newest, version_added)) {
      div.style = "display:none";
    } else if (version_removed && older_or_equal(version_removed, oldest)) {
      if (show_deleted_paragraphs) {
        div.style = "";
      } else {
        div.style = "display:none";
      }
    } else {
      div.style = "";
    }
  }
  for (var div of document.querySelectorAll(".diff-comment")) {
    for (var c of div.classList) {
      if (c.startsWith("changed-in-")) {
        version = c.split("-").slice(-3).map(x => parseInt(x));
      }
    }
    if (older_or_equal(version, oldest)) {
      div.style = "display:none";
    }
  }
}
window.onload = function () {
  for (var input of document.getElementsByTagName("input")) {
    input.onclick = meow;
  }
  for (var button of document.getElementsByTagName("button")) {
    const version = button.value;
    button.onclick = function () { show_version_diff(version); };
  }
  update_from_query();
}
addEventListener('popstate', update_from_query);
