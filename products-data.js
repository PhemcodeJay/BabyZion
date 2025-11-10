// products-data.js - Product catalog and filtering logic (USD version)

document.addEventListener('DOMContentLoaded', () => {
  const productsGrid = document.getElementById('products-grid');
  const filterBtns = document.querySelectorAll('.filter-btn');

  let allProducts = [];
  let currentCategory = new URLSearchParams(window.location.search).get('category') || '';

  // Fetch products from API
  fetch('/api/products')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(products => {
      console.log('Products loaded:', products.length);
      allProducts = products;

      // Auto-select category from URL
      if (currentCategory) {
        filterBtns.forEach(btn => {
          btn.classList.toggle('active', btn.dataset.category === currentCategory);
        });
      }

      renderProducts(currentCategory);
      updateCartCount();
    })
    .catch(error => {
      console.error('Error loading products:', error);
      productsGrid.innerHTML = `
        <p style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #ff6b9d; font-size: 1.1rem;">
          ⚠️ Unable to load products. Error: ${error.message}<br>
          Please make sure the server is running and try refreshing the page.
        </p>`;
    });

  // Filter buttons
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.dataset.category;
      renderProducts(currentCategory);

      // Update URL without page reload
      const url = new URL(window.location);
      if (currentCategory) {
        url.searchParams.set('category', currentCategory);
      } else {
        url.searchParams.delete('category');
      }
      window.history.pushState({}, '', url);
    });
  });

  function renderProducts(category) {
    productsGrid.innerHTML = '';

    const filtered = category 
      ? allProducts.filter(p => p.category === category) 
      : allProducts;

    if (filtered.length === 0) {
      productsGrid.innerHTML = `
        <p style="grid-column: 1 / -1; text-align: center; padding: 80px 20px; color: #999; font-size: 1.2rem;">
          No products found in this category.
        </p>`;
      return;
    }

    filtered.forEach(product => {
      const card = document.createElement('div');
      card.className = 'product-card';
      card.innerHTML = `
        <img src="${product.image || 'https://via.placeholder.com/300x300?text=Baby+Product'}" 
             alt="${product.name}" 
             loading="lazy"
             onerror="this.src='https://via.placeholder.com/300x300?text=No+Image'; this.onerror=null;">
        <h3>${escapeHtml(product.name)}</h3>
        <p class="product-description">${escapeHtml((product.description || '').substring(0, 100))}...</p>
        <div class="price">$${Number(product.price).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
        <button class="add-to-cart-btn" 
                data-id="${product.id}" 
                data-name="${escapeHtml(product.name)}" 
                data-price="${product.price}"
                data-image="${product.image || 'https://via.placeholder.com/300x300?text=Baby+Product'}">
          Add to Cart
        </button>
      `;
      productsGrid.appendChild(card);
    });

    // Re-attach Add to Cart listeners
    attachAddToCartListeners();
  }

  function attachAddToCartListeners() {
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();

        let cart = JSON.parse(localStorage.getItem('babyzion_cart') || '[]');
        const productData = {
          id: btn.dataset.id,
          name: btn.dataset.name,
          price: parseFloat(btn.dataset.price),
          image: btn.dataset.image,
          quantity: 1
        };

        const existing = cart.find(item => item.id === productData.id);
        if (existing) {
          existing.quantity += 1;
        } else {
          cart.push(productData);
        }

        localStorage.setItem('babyzion_cart', JSON.stringify(cart));
        updateCartCount();

        // Success feedback
        const originalText = btn.textContent;
        const originalBg = btn.style.background;
        btn.textContent = 'Added!';
        btn.style.background = '#28a745';
        btn.disabled = true;

        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.background = originalBg;
          btn.disabled = false;
        }, 2000);
      });
    });
  }

  function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('babyzion_cart') || '[]');
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  }

  // Simple HTML escape to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Optional: Listen for back/forward navigation
  window.addEventListener('popstate', () => {
    currentCategory = new URLSearchParams(window.location.search).get('category') || '';
    filterBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.category === currentCategory));
    renderProducts(currentCategory);
  });
});