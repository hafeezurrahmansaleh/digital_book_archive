import React from 'react';
import DataTable from 'react-data-table-component';
import DataTableExtensions from 'react-data-table-component-extensions';
import './DataTableContainer.css';

const DataTableContainer = ({ tableData, columns, data }) => {
    return (
        <div className="main">
            <DataTableExtensions {...tableData}>
                <DataTable
                    columns={columns}
                    data={data}
                    noDataComponent="No Data Available"
                    noHeader
                    defaultSortField="id"
                    defaultSortAsc={false}
                    pagination
                    highlightOnHover
                />
            </DataTableExtensions>
        </div>
    );
};

export default DataTableContainer;