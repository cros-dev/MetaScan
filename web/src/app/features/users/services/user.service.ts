import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { User, CreateUserRequest, UserFilters, UserListResponse } from '../models/user.model';

export type { User, CreateUserRequest, UserFilters, UserListResponse };

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.apiUrl}users/`;

  constructor(private http: HttpClient) {}

  getUsers(filters?: UserFilters): Observable<UserListResponse> {
    const params = this.buildParams(filters);
    return this.http.get<UserListResponse>(this.apiUrl, { params });
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}${id}/`);
  }

  createUser(userData: CreateUserRequest): Observable<User> {
    return this.http.post<User>(this.apiUrl, userData);
  }

  updateUser(id: number, userData: Partial<CreateUserRequest>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}${id}/`, userData);
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }

  private buildParams(filters?: UserFilters): HttpParams {
    let params = new HttpParams();

    if (filters?.role && filters.role !== '' && filters.role !== null) {
      params = params.set('role', filters.role);
    }
    if (filters?.is_active !== undefined) {
      params = params.set('is_active', filters.is_active.toString());
    }
    if (filters?.search && filters.search.trim() !== '') {
      params = params.set('search', filters.search);
    }

    return params;
  }
}
