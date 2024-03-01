
const getChartOptions = (percentageFull, percentageLate, percentageAbsent) => {
    return {
        series: [percentageFull,percentageAbsent, percentageLate],
        colors: ["#3b82f6", "#ef4444", "#fcd34d"],
        chart: {
        height: "380px",
        width: "100%",
        type: "radialBar",
        sparkline: {
            enabled: true,
        },
        },
        plotOptions: {
        radialBar: {
            track: {
            background: '#E5E7EB',
            },
            dataLabels: {
            show: false,
            },
            hollow: {
            margin: 0,
            size: "32%",
            }
        },
        },
        grid: {
        show: false,
        strokeDashArray: 4,
        padding: {
            left: 2,
            right: 2,
            top: -23,
            bottom: -20,
        },
        },
        labels: ["Full Attendance", "Absent", "Late"],
        legend: {
        show: true,
        position: "bottom",
        fontFamily: "Inter, sans-serif",
        },
        tooltip: {
        enabled: true,
        x: {
            show: false,
        },
        },
        yaxis: {
        show: false,
        labels: {
            formatter: function (value) {
            return value + '%';
            }
        }
        }
    }
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    const percentageFull = parseFloat(document.getElementById("full_day_percent").textContent);
    const percentageLate = parseFloat(document.getElementById("late_percent").textContent);
    const percentageAbsent = parseFloat(document.getElementById("absent_percent").textContent);

    if (!isNaN(percentageFull) && !isNaN(percentageLate) && !isNaN(percentageAbsent)) {
      if (document.getElementById("radial-chart") && typeof ApexCharts !== 'undefined') {
        const chart = new ApexCharts(document.querySelector("#radial-chart"), getChartOptions(percentageFull, percentageLate, percentageAbsent));
        chart.render();
      }
    }
  });
  