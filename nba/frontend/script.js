async function generateGraph() {
      const param1 = document.getElementById("param1").value;
      const param2 = document.getElementById("param2").value;

      const response = await fetch('http://127.0.0.1:5000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ param1, param2 })
      });

      const data = await response.json();
      document.getElementById("graph").src = data.image_url;
    }