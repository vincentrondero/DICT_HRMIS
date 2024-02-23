    let currentMonth;
    let currentYear;
    const daysInWeek = 7;

    function generateCalendar() {
        // Clear previous dates
        const calendarDates = document.getElementById('calendarDates');
        calendarDates.innerHTML = '';

        // Get the first day of the month
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        const startingDay = firstDayOfMonth.getDay();

        // Get the last day of the month
        const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);
        const totalDays = lastDayOfMonth.getDate();

        // Get the current day of the month
        const currentDay = new Date().getDate();

        // Populate the calendar
        for (let i = 0; i < startingDay; i++) {
            // Add placeholders for the days before the 1st of the month
            const emptyDay = document.createElement('div');
            emptyDay.classList.add('text-sm', 'text-gray-500', 'dark:text-gray-100', 'w-8', 'h-8', 'flex', 'items-center', 'justify-center');
            calendarDates.appendChild(emptyDay);
        }

        for (let day = 1; day <= totalDays; day++) {
            // Add the actual dates
            const dateElement = document.createElement('div');
            dateElement.classList.add('text-base', 'font-medium', 'text-center', 'w-8', 'h-8', 'flex', 'items-center', 'justify-center');

            // Highlight the current date
            if (day === currentDay && currentMonth === currentDate.getMonth() && currentYear === currentDate.getFullYear()) {
                dateElement.classList.add('bg-blue-500', 'text-white', 'rounded-full');
            }

            dateElement.textContent = day;
            calendarDates.appendChild(dateElement);
        }
    }


    function updateHeader() {
        document.getElementById('currentMonthYear').innerText = `${getMonthName(currentMonth)} ${currentYear}`;
    }

    function getMonthName(monthIndex) {
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        return months[monthIndex];
    }

    function updateCalendar() {
        generateCalendar();
    }

    function updateMonth(direction) {
        if (direction === 'next') {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
        } else if (direction === 'prev') {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
        }

        updateHeader();
        updateCalendar();
    }

    // Initialize current month and year
    const currentDate = new Date();
    currentMonth = currentDate.getMonth();
    currentYear = currentDate.getFullYear();

    // Update calendar on initial load
    updateHeader();
    updateCalendar();

    // Event listeners for next and previous month buttons
    document.getElementById('prevMonth').addEventListener('click', () => {
        updateMonth('prev');
    });

    document.getElementById('nextMonth').addEventListener('click', () => {
        updateMonth('next');
    });

