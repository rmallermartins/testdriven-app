import React from 'react';
import { shallow, mount } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import FormErrors from '../forms/FormErrors';
import { registerFormRules, loginFormRules } from '../forms/form-rules.js';

const testProps = [
  {
    formType: 'Register',
    formRules: registerFormRules,
  },
  {
    formType: 'Login',
    formRules: loginFormRules,
  }
]

describe('Form Errors', () => {
  testProps.forEach((el) => {
    const component = <FormErrors {...el} />;

    it(`FormErrors (with ${el.formType} form) renders properly`, () => {
      const wrapper = shallow(component);
      const ul = wrapper.find('ul');
      const li = wrapper.find('li');

      expect(ul.length).toBe(1);
      expect(li.length).toBe(el.formRules.length);
      el.formRules.forEach((rule, i) => {
        expect(li.get(i).props.children).toContain(rule.name);
      });
    });

    it(`FormErrors (with ${el.formType} form) renders a snapshot properly`, () => {
      const tree = renderer.create(
        <Router><FormErrors {...el} /></Router>
      ).toJSON();
      expect(tree).toMatchSnapshot();
    });
  });
});
