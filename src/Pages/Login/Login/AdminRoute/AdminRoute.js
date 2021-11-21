import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import ReactLoading from 'react-loading';
import useAuth from '../../../../hooks/useAuth';

const AdminRoute = ({ children, ...rest }) => {
    const { user, isLoading } = useAuth();
    if (isLoading) { return (
        <div className="d-flex align-items-center justify-content-center" style={{ height: '80vh' }}>
            <ReactLoading type={"spinningBubbles"} color={"#A99577"} height={100} width={100} />
        </div>
    ) }
    return (
        <Route
            {...rest}
            render={({ location }) =>
                user?.user_id ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/login",
                            state: { from: location }
                        }}
                    />
                )
            }
        />
    );
};

export default AdminRoute;