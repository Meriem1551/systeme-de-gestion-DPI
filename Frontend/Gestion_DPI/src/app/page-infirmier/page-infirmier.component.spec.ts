import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageInfirmierComponent } from './page-infirmier.component';

describe('PageInfirmierComponent', () => {
  let component: PageInfirmierComponent;
  let fixture: ComponentFixture<PageInfirmierComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageInfirmierComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PageInfirmierComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
