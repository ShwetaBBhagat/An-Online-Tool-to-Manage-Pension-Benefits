import { Routes } from '@angular/router';

import { AdminLoginComponent } from './admin/admin-login/admin-login.component';
import { AdminDashboardComponent } from './admin/admin-dashboard/admin-dashboard.component';
import { AllUsersComponent } from './admin/all-users/all-users.component';
import { UserStatementsComponent } from './admin/user-statements/user-statements.component';
import { ViewEmployersComponent } from './admin/view-employers/view-employers.component';
import { AddEmployerComponent } from './admin/add-employer/add-employer.component';
import { EmployerUsersComponent } from './admin/employer-users/employer-users.component';

import { EmployerLoginComponent } from './employer/employer-login/employer-login.component';
import { EmployerDashboardComponent } from './employer/employer-dashboard/employer-dashboard.component';
import { MyUsersComponent } from './employer/my-users/my-users.component';
import { EmployerProfileComponent } from './employer/employer-profile/employer-profile.component';
import { AddUserComponent } from './employer/add-user/add-user.component';
import { EmployerUserStatementsComponent } from './employer/user-statements/user-statements.component';
import { EmployerRequestResetComponent } from './employer/employer-request-reset/employer-request-reset.component';
import { EmployerResetPasswordComponent } from './employer/reset-password/reset-password.component';

import { RequestResetComponent } from './auth/request-reset/request-reset.component';
import { ResetPasswordComponent } from './auth/reset-password/reset-password.component';
import { DashboardComponent } from './auth/dashboard/dashboard.component';
import { ProfileComponent } from './auth/profile/profile.component';
import { StatementsComponent } from './auth/statements/statements.component';
import { UploadDocumentComponent } from './auth/upload-document/upload-document.component';
import { UserDocumentsComponent } from './auth/user-documents/user-documents.component';
import { AnalyticsComponent } from './auth/analytics/analytics.component';
import { LoginComponent } from './auth/login/login.component';
import { BeneficiaryComponent } from './auth/beneficiary/beneficiary.component';

import { HomeComponent } from './shared/home/home.component';
import { AboutComponent } from './shared/about/about.component';
import { FaqComponent } from './shared/faq/faq.component';

export const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full'}, 
  { path: 'about', component: AboutComponent },
  { path: 'faq', component: FaqComponent },

  { path: 'admin/login', component: AdminLoginComponent },
  { path: 'admin/dashboard',component: AdminDashboardComponent },
  { path: 'admin/all-users',component: AllUsersComponent },
  { path: 'admin/users/:id/statements', component: UserStatementsComponent },
  { path: 'admin/view-employers', component: ViewEmployersComponent },
  { path: 'admin/add-employer', component: AddEmployerComponent },
  { path: 'admin/employers/:id/users', component: EmployerUsersComponent },

  { path: 'employer/login', component: EmployerLoginComponent},  
  { path: 'employer/dashboard', component: EmployerDashboardComponent },
  { path: 'employer/my-users', component: MyUsersComponent },
  { path: 'employer/employer-profile', component: EmployerProfileComponent },
  { path: 'employer/add-user', component: AddUserComponent },
  { path: 'employer/user/:id/statements', component: EmployerUserStatementsComponent},
  { path: 'employer/employer-request-reset', component: EmployerRequestResetComponent},
  { path: 'employer/reset-password', component: EmployerResetPasswordComponent},

  { path: 'login', component: LoginComponent },
  { path: 'request-reset', component: RequestResetComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'statements', component: StatementsComponent },
  { path: 'upload-document', component: UploadDocumentComponent },
  { path: 'my-documents', component: UserDocumentsComponent },
  { path: 'analytics', component: AnalyticsComponent },
  { path: 'beneficiary', component: BeneficiaryComponent },

  { path: '**', redirectTo: 'login' }
];
