import React from 'react';
import DataTable from 'react-data-table-component';
import DataTableExtensions from 'react-data-table-component-extensions';
import CustomLoader from '../CustomLoader/CustomLoader';
import './DataTableContainer.css';

const DataTableContainer = ({ tableData, columns, data, pending }) => {
    return (
        <div className="main">
            <DataTableExtensions {...tableData}>
                <DataTable
                    columns={columns}
                    data={data}
                    progressPending={pending}
                    progressComponent={<CustomLoader />}
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