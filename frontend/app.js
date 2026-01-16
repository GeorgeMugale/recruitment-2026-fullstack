// BASE API
const API_BASE = "https://recruitment-2026-fullstack.onrender.com/api";

// declare elements
const select = document.getElementById("provinceSelect");
const results = document.getElementById("results");
const loader = document.getElementById("loader");
const searchInput = document.getElementById("constituency-search"); // Get this early

/**
 * Handles error states gracefully
 */
const handleError = (error) => {
  console.error("API Error:", error);
  results.innerHTML = `<li class="text-red-500 p-3">Failed to load data. Please try again.</li>`;
  loader.classList.add("hidden"); // Use Tailwind class to hide
};

/**
 * Fetches provinces
 */
async function initializeProvinces() {
  try {
    const response = await fetch(`${API_BASE}/provinces`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const provinces = await response.json();

    // CLEAR existing options to prevent duplicates
    select.innerHTML = "";

    // Add default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select a province";
    select.appendChild(defaultOption);

    // Add province options
    provinces.sort().forEach((province) => { // Added sort() for better UX
      const option = document.createElement("option");
      option.value = province;
      option.textContent = province;
      select.appendChild(option);
    });
  } catch (error) {
    handleError(error);
    select.disabled = true;
    select.innerHTML = `<option value="">Failed to load provinces</option>`;
  }
}

/**
 * Load Constituencies
 */
async function loadConstituencies(province) {
  // 1. Reset UI State
  results.innerHTML = "";
  searchInput.value = ""; // Clear search text when switching provinces
  
  if (!province) {
      searchInput.classList.add("hidden"); // Hide search if no province selected
      return;
  }

  // 2. Show Loader / Hide Search
  loader.classList.remove("hidden"); // Use Tailwind class
  searchInput.classList.add("hidden"); 

  try {
    const response = await fetch(
      `${API_BASE}/constituencies/${encodeURIComponent(province)}`
    );

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();

    // Handle different API return structures (list vs dict)
    const listData = data.constituencies || data;

    if (!listData || listData.length === 0) {
      results.innerHTML = `<li class="text-gray-500 p-3">No constituencies found.</li>`;
      return;
    }

    const fragment = document.createDocumentFragment();

    listData.sort().forEach((constituency) => {
      const li = document.createElement("li");
      li.textContent = constituency;
      
      // *** VITAL: ADD TAILWIND STYLING ***
      li.className = "p-3 bg-gray-50 rounded-lg hover:bg-blue-50 transition-colors text-gray-700 border border-gray-100 cursor-default";
      
      fragment.appendChild(li);
    });

    results.appendChild(fragment);
    
    // Show search input now that we have data
    searchInput.classList.remove("hidden");
    searchInput.focus();

  } catch (error) {
    handleError(error);
  } finally {
    loader.classList.add("hidden");
  }
}

// Event listener for Dropdown
select.addEventListener("change", () => {
  const province = select.value.trim();
  loadConstituencies(province);
});

// Event listener for Search
searchInput.addEventListener("input", (e) => {
  const searchTerm = e.target.value.toLowerCase();
  const items = results.getElementsByTagName("li");

  Array.from(items).forEach(item => {
    const text = item.textContent.toLowerCase();
    // Tailwind's 'hidden' class handles the display toggle
    if (text.includes(searchTerm)) {
      item.classList.remove("hidden");
    } else {
      item.classList.add("hidden");
    }
  });
});

// Initialize on load
document.addEventListener("DOMContentLoaded", initializeProvinces);