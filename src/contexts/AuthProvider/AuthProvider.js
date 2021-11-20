import React, { createContext } from 'react';
import useDjango from '../../hooks/useDjango';

export const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
    const allContexts = useDjango();
    return (
        <AuthContext.Provider value={allContexts}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;