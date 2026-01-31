function filterProducts() {
    const query = document.getElementById('search-bar').value.toLowerCase();
    const products = document.querySelectorAll('.product-card');
  
    products.forEach((product) => {
      const name = product.dataset.name.toLowerCase();
      if (name.includes(query)) {
        product.style.display = 'block';
      } else {
        product.style.display = 'none';
      }
    });
  }
  