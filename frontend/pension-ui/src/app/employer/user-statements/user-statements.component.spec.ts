import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserStatementsComponent } from './user-statements.component';

describe('UserStatementsComponent', () => {
  let component: UserStatementsComponent;
  let fixture: ComponentFixture<UserStatementsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserStatementsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserStatementsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
