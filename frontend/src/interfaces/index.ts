export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    first_name: string;
    last_name: string;
    username: string;
    id: string;
}

export interface IUserProfileUpdate {
    first_name?: string;
    last_name?: string;
    username?: string;
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}
