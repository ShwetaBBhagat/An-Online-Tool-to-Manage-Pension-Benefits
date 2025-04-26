import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { ForgotPasswordComponent } from './auth/forgot-password/forgot-password.component';
import { UserDashboardComponent } from './user/user-dashboard/user-dashboard.component';
import { AdminLoginComponent } from './admin/admin-login/admin-login.component';
import { AdminDashboardComponent } from './admin/admin-dashboard/admin-dashboard.component';
import { AllUsersComponent } from './admin/all-users/all-users.component';
import { UserStatementsComponent } from './admin/user-statements/user-statements.component';
import { ViewDocumentsComponent } from './admin/view-documents/view-documents.component';
import { ViewEmployersComponent } from './admin/view-employers/view-employers.component';
import { AddEmployerComponent } from './admin/add-employer/add-employer.component';
import { EmployerUsersComponent } from './admin/employer-users/employer-users.component';
import { EmployerLoginComponent } from './employer/employer-login/employer-login.component';
import { EmployerDashboardComponent } from './employer/employer-dashboard/employer-dashboard.component';
import { MyUsersComponent } from './employer/my-users/my-users.component';
import { EmployerProfileComponent } from './employer/employer-profile/employer-profile.component';
import { AddUserComponent } from './employer/add-user/add-user.component';
import { EmployerUserStatementsComponent } from './employer/user-statements/user-statements.component';
import { ViewEmployerDocumentsComponent } from './employer/view-documents/view-documents.component';
import { SetEmployerPasswordComponent } from './employer/set-password/set-password.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'user/dashboard', component: UserDashboardComponent },
  { path: 'admin/login', component: AdminLoginComponent },
  { path: 'admin/dashboard',component: AdminDashboardComponent },
  { path: 'admin/all-users',component: AllUsersComponent },
  { path: 'admin/users/:id/statements', component: UserStatementsComponent },
  { path: 'admin/view-documents', component: ViewDocumentsComponent },
  { path: 'admin/view-employers', component: ViewEmployersComponent },
  { path: 'admin/add-employer', component: AddEmployerComponent },
  { path: 'admin/employers/:id/users', component: EmployerUsersComponent },
  { path: 'employer/login', component: EmployerLoginComponent},  
  { path: 'employer/dashboard', component: EmployerDashboardComponent },
  { path: 'employer/my-users', component: MyUsersComponent },
  { path: 'employer/employer-profile', component: EmployerProfileComponent },
  { path: 'employer/add-user', component: AddUserComponent },
  { path: 'employer/user/:id/statements', component: EmployerUserStatementsComponent},
  { path: 'employer/documents', component: ViewEmployerDocumentsComponent },
  { path: 'employer/set-password', component: SetEmployerPasswordComponent },
  { path: '**', redirectTo: 'login' }
];
