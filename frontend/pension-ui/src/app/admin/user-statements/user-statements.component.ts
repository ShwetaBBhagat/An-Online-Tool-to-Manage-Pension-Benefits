import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-user-statements',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './user-statements.component.html',
  styleUrls: ['./user-statements.component.css']
})
export class UserStatementsComponent {
  userId = '';
  userName = '';
  statements: any[] = [];
  platformId = inject(PLATFORM_ID);


  // Filters
  start = '';
  end = '';
  minSalary = '';
  maxSalary = '';
  fundName = '';
  minPerf = '';
  maxPerf = '';

  constructor(private route: ActivatedRoute, private http: HttpClient) {
    this.userId = this.route.snapshot.paramMap.get('id') || '';
    this.fetchStatements();
  }
  
  generateStatement() {
    const confirmGen = confirm("Are you sure you want to auto-generate a new pension statement for this user?");
    if (!confirmGen) return;
  
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };
  
    this.http.post<any>(
      `http://127.0.0.1:5000/api/admin/user/${this.userId}/statements`,
      {}, // no payload needed
      { headers }
    ).subscribe({
      next: (res) => {
        alert(`✅ Statement generated for ${res.user} (Pot: £${res.pot_value})`);
        this.fetchStatements(); // reload the table
      },
      error: (err) => {
        const message = err.error?.error || 'Something went wrong';
        alert(`❌ Failed to generate statement: ${message}`);
      }
    });
  }
  
  fetchStatements() {
    if (!isPlatformBrowser(this.platformId)) {
      return; // Skip SSR
    }

    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };

    const params: any = {};
    if (this.start) params.start = this.start;
    if (this.end) params.end = this.end;
    if (this.minSalary) params.min_salary = this.minSalary;
    if (this.maxSalary) params.max_salary = this.maxSalary;
    if (this.fundName) params.fund_name = this.fundName;
    if (this.minPerf) params.min_performance = this.minPerf;
    if (this.maxPerf) params.max_performance = this.maxPerf;

    this.http.get<any>(`http://127.0.0.1:5000/api/admin/user/${this.userId}/statements`, {
      headers,
      params
    }).subscribe({
      next: (res) => {
        this.statements = res.statements || [];
        this.userName = res.user_name;
      },
      error: (err) => {
        console.error('Error fetching statements:', err);
      }
    });
  }

  deleteStatement(statementId: number) {
    const confirmDelete = confirm(`Are you sure you want to delete statement ID ${statementId}?`);
    if (!confirmDelete) return;
  
    const token = localStorage.getItem('adminToken');
    const headers = { Authorization: `Bearer ${token}` };
  
    this.http.delete<any>(`http://127.0.0.1:5000/api/admin/statements/${statementId}`, { headers }).subscribe({
      next: (res) => {
        alert(res.message);
        this.fetchStatements(); // Refresh table
      },
      error: (err) => {
        const msg = err.error?.error || 'Failed to delete statement';
        alert(`❌ ${msg}`);
      }
    });
  }
  
  resetFilters() {
    this.start = '';
    this.end = '';
    this.minSalary = '';
    this.maxSalary = '';
    this.fundName = '';
    this.minPerf = '';
    this.maxPerf = '';
    this.fetchStatements();
  }
}
