import React, { useMemo } from 'react';
import { Table, Badge, Button } from 'react-bootstrap';
import { useTable, useSortBy } from 'react-table';
import { FaPhone, FaEdit, FaComment } from 'react-icons/fa';

const LeadTable = ({ leads, onEditLead, onAddNote }) => {
  // Define table columns
  const columns = useMemo(() => [
    {
      Header: 'Name',
      accessor: 'name',
    },
    {
      Header: 'Phone',
      accessor: 'phone',
      Cell: ({ value }) => (
        <div className="d-flex align-items-center">
          <a href={`tel:${value}`} className="me-2">
            <FaPhone className="text-primary" />
          </a>
          {value}
        </div>
      ),
    },
    {
      Header: 'Email',
      accessor: 'email',
    },
    {
      Header: 'Status',
      accessor: 'status',
      Cell: ({ value }) => {
        let badgeClass = '';
        
        switch(value) {
          case 'NEW':
            badgeClass = 'bg-primary';
            break;
          case 'SENT':
            badgeClass = 'bg-info';
            break;
          case 'REPLIED':
            badgeClass = 'bg-warning';
            break;
          case 'BOOKED':
            badgeClass = 'bg-success';
            break;
          default:
            badgeClass = 'bg-secondary';
        }
        
        return <Badge className={badgeClass}>{value}</Badge>;
      },
    },
    {
      Header: 'Created',
      accessor: 'created_at',
      Cell: ({ value }) => new Date(value).toLocaleDateString(),
    },
    {
      Header: 'Actions',
      id: 'actions',
      Cell: ({ row }) => (
        <div className="d-flex gap-2">
          <Button 
            variant="outline-primary" 
            size="sm" 
            onClick={(e) => {
              e.stopPropagation();
              onEditLead(row.original);
            }}
          >
            <FaEdit />
          </Button>
          <Button 
            variant="outline-secondary" 
            size="sm" 
            onClick={(e) => {
              e.stopPropagation();
              onAddNote(row.original);
            }}
          >
            <FaComment />
          </Button>
        </div>
      ),
    },
  ], [onEditLead, onAddNote]);

  // Memoize data to avoid unnecessary renders
  const data = useMemo(() => leads, [leads]);

  // Create table instance
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
    },
    useSortBy
  );

  // Render expanded row with notes
  const renderNotesRow = (lead) => {
    if (!lead.notes || lead.notes.length === 0) {
      return (
        <div className="text-muted py-2">
          No notes yet. Click the comment button to add a note.
        </div>
      );
    }
    
    return lead.notes.map((note) => (
      <div key={note.id} className="note-row py-1">
        <div>{note.content}</div>
        <div className="note-timestamp">
          {new Date(note.created_at).toLocaleString()}
        </div>
      </div>
    ));
  };

  // Function to handle row click for expansion
  const [expandedRow, setExpandedRow] = React.useState(null);

  return (
    <div className="table-responsive">
      <Table className="lead-table" {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                  {column.render('Header')}
                  <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? ' 🔽'
                        : ' 🔼'
                      : ''}
                  </span>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            const isExpanded = expandedRow === row.original.id;
            
            return (
              <React.Fragment key={row.original.id}>
                <tr 
                  {...row.getRowProps()}
                  onClick={() => setExpandedRow(isExpanded ? null : row.original.id)}
                  className={isExpanded ? 'table-active' : ''}
                >
                  {row.cells.map(cell => (
                    <td {...cell.getCellProps()}>
                      {cell.render('Cell')}
                    </td>
                  ))}
                </tr>
                {isExpanded && (
                  <tr>
                    <td colSpan={columns.length} className="bg-light">
                      <div className="p-3">
                        <h6>Notes</h6>
                        {renderNotesRow(row.original)}
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            );
          })}
          {rows.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="text-center py-4">
                No leads found. Add a new lead to get started.
              </td>
            </tr>
          )}
        </tbody>
      </Table>
    </div>
  );
};

export default LeadTable;
