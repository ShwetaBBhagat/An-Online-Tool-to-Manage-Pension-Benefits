import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-statements',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './statements.component.html',
  styleUrls: ['./statements.component.css']
})
export class StatementsComponent {
  statements: any[] = [];

  constructor(private http: HttpClient) {
    this.loadStatements();
  }

  loadStatements() {
    const token = localStorage.getItem('userToken');

    if (!token) {
      console.error('No token found');
      return;
    }

    this.http.get<any>('http://127.0.0.1:5000/api/auth/user/statements', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).subscribe({
      next: (res) => {
        if (res.status === 'success') {
          this.statements = res.data;
        }
      },
      error: (err) => {
        console.error('Error fetching statements:', err);
      }
    });
  }

  // ✅ New method to download PDF
  downloadPDF(statementId: number) {
    const token = localStorage.getItem('userToken');

    this.http.get(`http://127.0.0.1:5000/api/auth/user/statements/${statementId}/download`, {
      headers: {
        Authorization: `Bearer ${token}`
      },
      responseType: 'blob' // very important!
    }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `statement_${statementId}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (err) => {
        console.error('Error downloading statement:', err);
      }
    });
  }
}
