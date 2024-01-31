function showTable(tableId) {
    const activeButton = document.getElementById('activeButton');
    const archiveButton = document.getElementById('archiveButton');
    const activeTable = document.getElementById('activeTable');
    const archiveTable = document.getElementById('archiveTable');

    if (tableId === 'activeTable') {
        // Show Active table
        activeTable.classList.remove('hidden');
        archiveTable.classList.add('hidden');
        activeButton.classList.add('bg-custom-blue');
        activeButton.classList.add('text-white');
        activeButton.classList.remove('bg-white');
        archiveButton.classList.add('bg-custom-bg');
        archiveButton.classList.remove('bg-custom-blue');
        archiveButton.classList.remove('text-white');
    } else if (tableId === 'archiveTable') {
        // Show Archive table
        activeTable.classList.add('hidden');
        archiveTable.classList.remove('hidden');
        activeButton.classList.add('bg-custom-bg');
        activeButton.classList.remove('text-white');
        activeButton.classList.remove('bg-custom-blue');
        archiveButton.classList.add('bg-custom-blue');
        archiveButton.classList.add('text-white');
        archiveButton.classList.remove('bg-white');
    }
}