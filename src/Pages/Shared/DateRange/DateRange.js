import React from 'react';
import ReactDatePicker from 'react-datepicker';

const DateRange = ({ startDate, endDate, handleDateRange }) => {
    
    return (
        <div className="text-start mb-3" style={{ maxWidth: 300 }}>
            <div class="d-flex border rounded-pill border-2">
                <div class="px-4 fs-6 fw-bold d-flex align-items-center bg-light rounded-pill" id="inputGroup-sizing-default">Range</div>
                <ReactDatePicker
                    className="border-0"
                    selectsRange={true}
                    startDate={startDate}
                    endDate={endDate}
                    shouldCloseOnSelect={false}
                    onChange={(update) => {
                        handleDateRange(update)
                    }}
                    isClearable={true}
                />
            </div>
        </div>
    );
};

export default DateRange;