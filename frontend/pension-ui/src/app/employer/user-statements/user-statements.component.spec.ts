import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmployerUserStatementsComponent } from './user-statements.component';

describe('UserStatementsComponent', () => {
  let component: EmployerUserStatementsComponent;
  let fixture: ComponentFixture<EmployerUserStatementsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployerUserStatementsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EmployerUserStatementsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
