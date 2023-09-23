// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
  /**
   * Retrieve the value of a cell in a table row.
   * @param {HTMLElement} tr - The table row element.
   * @param {number} idx - The index of the cell within the row.
   * @return {number|string|null} - The value of the cell, parsed appropriately.
   */
  const getCellValue = (tr, idx) => {
    const cell = tr.children[idx];
    if (!cell) return null;
    let value = cell.innerText || cell.textContent;

    // Convert percentages to decimal numbers
    if (value.includes('%')) {
      return parseFloat(value.replace('%', '')) / 100;
    }

    // Remove dollar signs and commas for easier parsing
    value = value.replace(/[$,]/g, '');
    return isNaN(value) ? (value === 'nan' ? 0 : value) : parseFloat(value);
  };

  /**
   * Generate a comparison function for sorting table rows.
   * @param {number} idx - The index of the cell to sort by.
   * @param {boolean} asc - True for ascending, false for descending.
   * @return {function} - A comparison function.
   */
  const comparer = (idx, asc) => (a, b) => {
    const valA = getCellValue(asc ? a : b, idx) || 0;
    const valB = getCellValue(asc ? b : a, idx) || 0;

    // Perform numeric or string comparison as needed
    if (typeof valA === 'number' && typeof valB === 'number') {
      return valA - valB;
    } else if (valA === null || valB === null) {
      return valA ? -1 : 1;
    } else {
      return String(valA).localeCompare(String(valB));
    }
  };

  // Find each table with the class 'sortable-table' and attach sorting logic
  document.querySelectorAll('.sortable-table thead').forEach((thead) => {
    thead.querySelectorAll('th').forEach((th) => {
      let sortAsc = true; // Keep track of the current sort direction
      th.addEventListener('click', () => {
        const table = th.closest('table');
        const idx = Array.from(th.parentNode.children).indexOf(th);

        // Sort the rows based on the clicked header
        const sortedRows = Array.from(table.querySelectorAll('tbody tr')).sort(
          comparer(idx, sortAsc)
        );

        // Toggle the sort direction for the next click
        sortAsc = !sortAsc;

        // Append sorted rows back to the table
        table.querySelector('tbody').append(...sortedRows);
      });
    });
  });
});
