import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import useAuth from '../../../../hooks/useAuth';
import CustomLoader from '../../../Shared/CustomLoader/CustomLoader';

const AdminRoute = ({ children, ...rest }) => {
    const { user, isLoading } = useAuth();
    if (isLoading) { return (
        <div className="d-flex align-items-center justify-content-center" style={{ height: '80vh' }}>
            <CustomLoader />
        </div>
    ) }
    return (
        <Route
            {...rest}
            render={({ location }) =>
                user?.is_admin || user?.is_superuser ? (
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