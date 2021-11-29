import React from 'react';
import ReactLoading from 'react-loading';


const CustomLoader = () => {
    return (
        <div className="d-flex align-items-center justify-content-center">
            <ReactLoading type={"spin"} color={"#8270C1"} height={80} width={80} />
        </div>
    );
};

export default CustomLoader;