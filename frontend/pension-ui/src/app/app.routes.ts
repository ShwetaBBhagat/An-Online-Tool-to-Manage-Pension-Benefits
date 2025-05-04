import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
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
import { SetPasswordComponent } from './employer/set-password/set-password.component';
import { RequestResetComponent } from './auth/request-reset/request-reset.component';
import { ResetPasswordComponent } from './auth/reset-password/reset-password.component';
import { DashboardComponent } from './auth/dashboard/dashboard.component';
import { ProfileComponent } from './auth/profile/profile.component';
import { StatementsComponent } from './auth/statements/statements.component';
import { UploadDocumentComponent } from './auth/upload-document/upload-document.component';
import { UserDocumentsComponent } from './auth/user-documents/user-documents.component';
import { AnalyticsComponent } from './auth/analytics/analytics.component';
import { HomeComponent } from './shared/home/home.component';
export const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full'}, 
  { path: 'login', component: LoginComponent },
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
  { path: 'employer/set-password', component: SetPasswordComponent },
  { path: 'request-reset', component: RequestResetComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'statements', component: StatementsComponent },
  { path: 'upload-document', component: UploadDocumentComponent },
  { path: 'my-documents', component: UserDocumentsComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: '**', redirectTo: 'login' }
];
