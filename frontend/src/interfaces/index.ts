export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    first_name: string;
    last_name: string;
    username: string;
    id: string;
    created_date: string;
    updated_date: string;
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

export interface IOffenders {
    id: string;
    state: string;
    sex: string;
    names: any[];
    addresses: any[];
    dob: any;
    is_deleted: boolean;
    created_date: string;
    updated_date: string;
    age: number;
    cases: any[];
}

export interface IOffenderPageModel {
    current_page: number;
    items: IOffenders[];
    limit: number;
    next: string;
    prev: string;
    total_items: number;
    total_pages: number;
}

export interface IUserPageModel {
    current_page: number;
    items: IUserProfile[];
    limit: number;
    next: string;
    prev: string;
    total_items: number;
    total_pages: number;
}
