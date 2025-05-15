import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-employer-user-statements',
  standalone: true,
  imports: [CommonModule, HttpClientModule, RouterModule],
  templateUrl: './user-statements.component.html',
  styleUrls: ['./user-statements.component.css']
})
export class EmployerUserStatementsComponent {
  userId = '';
  statements: any[] = [];
  errorMsg = '';

  constructor(private route: ActivatedRoute, private http: HttpClient) {
    this.userId = this.route.snapshot.paramMap.get('id') || '';
    this.fetchStatements();
  }

  fetchStatements() {
    const token = localStorage.getItem('employerToken');
    const headers = { Authorization: `Bearer ${token}` };

    this.http.get<any>(`http://127.0.0.1:5000/api/employer/user/${this.userId}/statements`, { headers }).subscribe({
      next: (res) => {
        this.statements = res.statements || [];
      },
      error: (err) => {
        this.errorMsg = err.error?.error || 'Failed to load statements.';
      }
    });
  }
}
