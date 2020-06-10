// Start dark mode
const themeSwitch = document.getElementById("themeSwitch");

let darkMode = localStorage.getItem('darkMode')

const enableDarkMode = () => {
  document.body.classList.add("dark-mode");
  localStorage.setItem("darkMode", "enabled")
}

const disableDarkMode = () => {
  document.body.classList.remove("dark-mode");
  localStorage.setItem("darkMode", null)
}

if (darkMode === "enabled") {
  enableDarkMode();
  themeSwitch.checked = true;
}

themeSwitch.addEventListener("click", () => {
  darkMode = localStorage.getItem('darkMode');
  if (darkMode !== "enabled") {
    enableDarkMode();
  } else {
    disableDarkMode();
  }
});

// End dark mode

// Start modal open and closening
var modal_close = document.getElementById("modal_close");
var modal_open = document.getElementById("modal_open");
var modal = document.getElementById("cfg_modal");

modal_close.addEventListener("click", function () {
  modal.classList.add("hidden");
});

modal_open.addEventListener("click", function () {
  modal.classList.remove("hidden");
});

// End modal

// Start charts responsiveness on window resize

window.addEventListener('resize', () => {
  drawPieChart();
  drawBarChart();
  drawColumnChart();
  drawTrendlineChart();
  drawLineChart();
});
