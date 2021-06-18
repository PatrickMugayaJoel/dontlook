import dateutil.parser

from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator

from mayan.apps.documents.models import Document
from mayan.apps.views.forms import DynamicForm
from mayan.apps.views.generics import FormView, SingleObjectListView
from mayan.apps.views.mixins import ExternalObjectMixin

from ..forms import WorkflowInstanceTransitionSelectForm
from ..icons import icon_workflow_instance_detail, icon_workflow_template_list
from ..links import link_workflow_instance_transition
from ..literals import FIELD_TYPE_MAPPING, WIDGET_CLASS_MAPPING
from ..models import WorkflowInstance
from ..permissions import permission_workflow_view


class WorkflowInstanceListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'no_results_icon': icon_workflow_template_list,
            'no_results_text': _(
                'Assign workflows to the document type of this document '
                'to have this document execute those workflows. '
            ),
            'no_results_title': _(
                'There are no workflows for this document'
            ),
            'object': self.external_object,
            'title': _(
                'Workflows for document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.workflows.all()


class WorkflowInstanceDetailView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = WorkflowInstance
    external_object_permission = permission_workflow_view
    external_object_pk_url_kwarg = 'workflow_instance_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'navigation_object_list': ('object', 'workflow_instance'),
            'no_results_icon': icon_workflow_instance_detail,
            'no_results_main_link': link_workflow_instance_transition.resolve(
                context=RequestContext(
                    dict_={'object': self.external_object},
                    request=self.request
                )
            ),
            'no_results_text': _(
                'This view will show the state changes as a workflow '
                'instance is transitioned.'
            ),
            'no_results_title': _(
                'There are no details for this workflow instance'
            ),
            'object': self.external_object.document,
            'title': _('Detail of workflow: %(workflow)s') % {
                'workflow': self.external_object
            },
            'workflow_instance': self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.log_entries.order_by('-datetime')


class WorkflowInstanceTransitionExecuteView(FormView):
    form_class = DynamicForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        form_data = form.cleaned_data
        comment = form_data.pop('comment')

        self.get_workflow_instance().do_transition(
            comment=comment, extra_data=form_data,
            transition=self.get_workflow_transition(), user=self.request.user,
        )
        messages.success(
            self.request, _(
                'Document "%s" transitioned successfully'
            ) % self.get_workflow_instance().document
        )
        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.get_workflow_instance().document,
            'submit_label': _('Submit'),
            'title': _(
                'Execute transition "%(transition)s" for workflow: %(workflow)s'
            ) % {
                'transition': self.get_workflow_transition(),
                'workflow': self.get_workflow_instance(),
            },
            'workflow_instance': self.get_workflow_instance(),
        }

    def get_form_extra_kwargs(self):
        schema = {
            'fields': {
                'comment': {
                    'label': _('Comment'),
                    'class': 'django.forms.CharField', 'kwargs': {
                        'help_text': _(
                            'Optional comment to attach to the transition.'
                        ),
                        'required': False,
                    }
                }
            },
            'widgets': {
                'comment': {
                    'class': 'django.forms.widgets.Textarea',
                    'kwargs': {
                        'attrs': {
                            'rows': 3
                        }
                    }
                }
            }
        }

        for field in self.get_workflow_transition().fields.all():
            schema['fields'][field.name] = {
                'class': FIELD_TYPE_MAPPING[field.field_type],
                'help_text': field.help_text,
                'label': field.label,
                'required': field.required,
            }
            if field.widget:
                schema['widgets'][field.name] = {
                    'class': WIDGET_CLASS_MAPPING[field.widget],
                    'kwargs': field.get_widget_kwargs()
                }

        return {'schema': schema}

    def get_success_url(self):
        return self.get_workflow_instance().get_absolute_url()

    def get_workflow_instance(self):
        return get_object_or_404(
            klass=WorkflowInstance, pk=self.kwargs['workflow_instance_id']
        )

    def get_workflow_transition(self):
        return get_object_or_404(
            klass=self.get_workflow_instance().get_transition_choices(
                _user=self.request.user
            ), pk=self.kwargs['workflow_transition_id']
        )


class WorkflowInstanceTransitionSelectView(ExternalObjectMixin, FormView):
    external_object_class = WorkflowInstance
    external_object_pk_url_kwarg = 'workflow_instance_id'
    form_class = WorkflowInstanceTransitionSelectForm
    template_name = 'appearance/generic_form.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='document_states:workflow_instance_transition_execute',
                kwargs={
                    'workflow_instance_id': self.external_object.pk,
                    'workflow_transition_id': form.cleaned_data['transition'].pk
                }
            )
        )

    def get_extra_context(self):
        return {
            'navigation_object_list': ('object', 'workflow_instance'),
            'object': self.external_object.document,
            'submit_label': _('Select'),
            'title': _(
                'Select transition for workflow: %s'
            ) % self.external_object,
            'workflow_instance': self.external_object,
        }

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user,
            'workflow_instance': self.external_object
        }

class WorkflowDocumentsReport(View):
    template_name = 'appearance/workflow_report.html'

    def get(self, request, *args, **kwargs): # {kwargs.get("workflow_id")} claims_workflow_id is '13'
        trans = []

        transitions = Document.objects.raw(f"""SELECT swi.document_id AS id, json_agg(swil.datetime) AS dates,
                json_agg(sws_d.label) AS dest
                FROM document_states_workflowinstance swi, document_states_workflowinstancelogentry swil,
                document_states_workflowtransition swt,
                document_states_workflowstate sws_d
                WHERE
                    swi.workflow_id = {request.GET.get('workflow_id', 1)}
                    AND swil.workflow_instance_id = swi.id
                    AND swil.transition_id = swt.id
                    AND swt.destination_state_id = sws_d.id
                group by swi.document_id
                order by swi.document_id desc;""")

        for transition in transitions:
            if len(transition.dates) > 2:
                tempObj = {}
                tempObj['id'] = transition.id
                tempObj['url'] = f"/documents/documents/{transition.id}/preview/"
                states = []

                for i in range(len(transition.dates)):
                    states.append({
                        "date":dateutil.parser.isoparse(transition.dates[i]).strftime("%a %d, %b %y"),
                        "state":transition.dest[i],
                        "sortie": transition.dates[i]
                    })

                tempObj['states'] = sorted(states, key = lambda i: i['sortie'])
                states.clear()
                trans.append(tempObj)

        paginator = Paginator(trans, 15)
        page_number = request.GET.get('page', 1)
        workflow_id = request.GET.get('workflow_id', 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'title': 'Medical Refund workflow' if (workflow_id == '13') else 'Claims workflow',
            'page_obj': page_obj, "workflow_id": workflow_id
        }
        return render(request, self.template_name, context)
