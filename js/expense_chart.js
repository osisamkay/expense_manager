document.addEventListener('DOMContentLoaded', function () {
  var ctx = document.getElementById('expenseChart').getContext('2d');
  var data = {
    labels: [],
    datasets: [{
      label: 'Expense Amount',
      backgroundColor: [], // Different colors for each segment
      borderWidth: 1,
      data: []
    }]
  };

  {% for expense in all_total_expenses %}
    {% for category, amount in expense.items() %}
      {% if category != "All Expenses" %}
        data.labels.push("{{ category }}");
        data.datasets[0].data.push("{{ amount }}");
        // Generate random color for each segment
        var randomColor = '#' + Math.floor(Math.random()*16777215).toString(16);
        data.datasets[0].backgroundColor.push(randomColor);
      {% endif %}
    {% endfor %}
  {% endfor %}

  new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        position: 'bottom',
      },
    }
  });
});
